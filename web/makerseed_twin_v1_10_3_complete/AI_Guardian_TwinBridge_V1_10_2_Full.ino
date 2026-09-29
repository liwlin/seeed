/*
  AI 碉楼守护者 · Twin Bridge V1.10.2 Full
  Grove Beginner Kit for Arduino / Seeeduino Lotus

  目标：Part 1 数字孪生完整真机桥接

  真机功能：
  - 输入：A0 旋钮、A6 光线、A2 声音、D6 按键
  - 温湿度：自动识别 DHT20（新版 I2C 0x38）或 DHT11（旧版 D3）
  - 气压：自动识别 SPA06-003（新版）或 BMP280（旧版）
  - 三轴加速度：LIS3DHTR @ I2C 0x19
  - 输出：D4 LED、D5 无源蜂鸣器、128x64 OLED
  - OLED：支持可靠位图分块传输（逐块 ACK + 重试），可显示网页渲染的中文
  - Web Serial：115200 baud，JSON Lines 上报 + 短文本命令下发

  Arduino 库：
  1) Grove Temperature And Humidity Sensor 2.0.2 (Seeed Studio)
  2) Seeed Arduino SPA06 (Seeed Studio)
  3) Grove - Barometer Sensor BMP280 1.0.1 (Seeed Studio)
  4) Grove-3-Axis-Digital-Accelerometer-2g-to-16g-LIS3DHTR (Seeed Studio)
  5) U8g2 (oliver)

  OLED 可靠位图协议：
  - OBEGIN                         开始传输；先清屏，完成后 ACK
  - OT <seq> <page> <tile> <hex>  每块 16 bytes；写完后带 seq ACK
  - OEND                           结束传输，恢复状态上报
  - OLEDCLR                        单独可靠清屏

  每条 OT 传 2 个 U8X8 tile = 16 bytes，命令长度小于 AVR 64-byte RX 缓冲。
  seq: 0..63, page: 0..7, tile: 0,2,4,...14
  重发同一 seq 是幂等的：同一 tile 只会被相同数据覆盖。
*/

#include <Arduino.h>
#include <Wire.h>
#include <string.h>
#include "Grove_Temperature_And_Humidity_Sensor.h"
#include "LIS3DHTR.h"
#include "SPL07-003.h"
#include "Seeed_BMP280.h"
#include <U8x8lib.h>

// ==================== 板载接口 ====================
const uint8_t LED_PIN       = 4;   // D4
const uint8_t BUZZER_PIN    = 5;   // D5 PWM
const uint8_t BUTTON_PIN    = 6;   // D6
const uint8_t DHT11_PIN     = 3;   // 旧版温湿度 D3

// 直接使用 ADC 通道，兼容 Arduino Uno 板型编译。
const uint8_t KNOB_ADC      = 0;   // A0
const uint8_t SOUND_ADC     = 2;   // A2
const uint8_t LIGHT_ADC     = 6;   // ADC6 / A6

const bool BUTTON_ACTIVE_HIGH = true;

// ==================== 环境传感器版本 ====================
enum TempKind : uint8_t {
  TEMP_NONE = 0,
  TEMP_DHT20,
  TEMP_DHT11
};

enum PressureKind : uint8_t {
  PRESS_NONE = 0,
  PRESS_SPA06,
  PRESS_BMP280
};

#define DHTTYPE20 DHT20
DHT dht20(DHTTYPE20);
DHT dht11(DHT11_PIN, DHT11);

LIS3DHTR<TwoWire> LIS;
SPL07_003 spl;
BMP280 bmp;
U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);

TempKind tempKind = TEMP_NONE;
PressureKind pressureKind = PRESS_NONE;

bool tempOk = false;
bool tempHasReading = false;
bool pressureOk = false;
bool pressureHasReading = false;
bool accelOk = false;
bool oledOk = false;
uint8_t pressureAddress = 0;

float temperatureC = 0.0f;
float humidityRH = 0.0f;
float pressureHpa = 0.0f;
float accelX = 0.0f;
float accelY = 0.0f;
float accelZ = 0.0f;

uint16_t tempSeq = 0;
uint16_t pressureSeq = 0;

// ==================== 串口与调度 ====================
const uint32_t SERIAL_BAUD = 115200;
const uint16_t STATE_INTERVAL_MS = 50;      // 20 Hz 快通道
const uint16_t DHT20_INTERVAL_MS = 1200;    // DHT20 慢通道
const uint16_t DHT11_INTERVAL_MS = 2100;    // DHT11 官方库 2 s 缓存节奏
const uint16_t PRESS_INTERVAL_MS = 250;     // 4 Hz

unsigned long lastStateMs = 0;
unsigned long lastTempMs = 0;
unsigned long lastPressureMs = 0;

bool ledState = false;
uint16_t buzzerFrequency = 0;
bool oledTransferActive = false;

// 所有下行命令控制在 64 字节以内；112 留作本地解析余量。
char commandBuffer[112];
uint8_t commandLength = 0;

// ==================== 工具函数 ====================
bool probeI2C(uint8_t address) {
  Wire.beginTransmission(address);
  return Wire.endTransmission() == 0;
}

bool readI2CRegister(uint8_t address, uint8_t reg, uint8_t &value) {
  Wire.beginTransmission(address);
  Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(address, (uint8_t)1) != 1) return false;
  value = Wire.read();
  return true;
}

void setLed(bool on) {
  ledState = on;
  digitalWrite(LED_PIN, on ? HIGH : LOW);
}

void setBuzzer(uint16_t frequency) {
  if (frequency == 0) {
    buzzerFrequency = 0;
    noTone(BUZZER_PIN);
    digitalWrite(BUZZER_PIN, LOW);
    return;
  }
  frequency = constrain(frequency, (uint16_t)31, (uint16_t)5000);
  buzzerFrequency = frequency;
  tone(BUZZER_PIN, frequency);
}

uint16_t readSoundLevel() {
  uint16_t minValue = 1023;
  uint16_t maxValue = 0;
  const unsigned long startUs = micros();
  while ((unsigned long)(micros() - startUs) < 4000UL) {
    const uint16_t value = analogRead(SOUND_ADC);
    if (value < minValue) minValue = value;
    if (value > maxValue) maxValue = value;
  }
  return maxValue - minValue;
}

const __FlashStringHelper* tempKindText() {
  if (tempKind == TEMP_DHT20) return F("DHT20");
  if (tempKind == TEMP_DHT11) return F("DHT11");
  return F("NONE");
}

const __FlashStringHelper* pressureKindText() {
  if (pressureKind == PRESS_SPA06) return F("SPA06-003");
  if (pressureKind == PRESS_BMP280) return F("BMP280");
  return F("NONE");
}

// ==================== OLED ====================
void oledClear() {
  if (!oledOk) return;
  u8x8.clearDisplay();
}

// 保留 ASCII 文本命令，便于串口监视器手工测试。
void oledWriteText(const char* text) {
  if (!oledOk) return;
  u8x8.clearDisplay();
  u8x8.setFont(u8x8_font_chroma48medium8_r);

  char line[17];
  uint8_t col = 0;
  uint8_t row = 0;

  while (*text && row < 8) {
    const uint8_t c = (uint8_t)(*text++);
    if (c == '|') {
      line[col] = '\0';
      u8x8.setCursor(0, row);
      u8x8.print(line);
      row++;
      col = 0;
      continue;
    }
    line[col++] = (c >= 32 && c <= 126) ? (char)c : '?';
    if (col >= 16) {
      line[16] = '\0';
      u8x8.setCursor(0, row);
      u8x8.print(line);
      row++;
      col = 0;
    }
  }

  if (row < 8 && col > 0) {
    line[col] = '\0';
    u8x8.setCursor(0, row);
    u8x8.print(line);
  }
}

int8_t hexNibble(char c) {
  if (c >= '0' && c <= '9') return c - '0';
  if (c >= 'A' && c <= 'F') return c - 'A' + 10;
  if (c >= 'a' && c <= 'f') return c - 'a' + 10;
  return -1;
}

bool oledDrawTileCommand(char* args, int16_t &seqOut) {
  seqOut = -1;
  if (!oledOk || !oledTransferActive) return false;

  char* seqToken = strtok(args, " ");
  char* rowToken = strtok(NULL, " ");
  char* tileToken = strtok(NULL, " ");
  char* hexToken = strtok(NULL, " ");
  if (!seqToken || !rowToken || !tileToken || !hexToken) return false;

  const int seq = atoi(seqToken);
  const int row = atoi(rowToken);
  const int tileX = atoi(tileToken);
  seqOut = seq;
  if (seq < 0 || seq > 63 || row < 0 || row > 7 || tileX < 0 || tileX > 14 || (tileX % 2) != 0) return false;
  if (strlen(hexToken) != 32) return false;

  uint8_t data[16];
  for (uint8_t i = 0; i < 16; i++) {
    const int8_t hi = hexNibble(hexToken[i * 2]);
    const int8_t lo = hexNibble(hexToken[i * 2 + 1]);
    if (hi < 0 || lo < 0) return false;
    data[i] = (uint8_t)((hi << 4) | lo);
  }

  // U8X8 直接写 2 个 8x8 tile，不占用 1 KB 全屏 framebuffer。
  // 相同 seq 的重发会覆盖同一 tile，因此重试是安全的。
  u8x8.drawTile((uint8_t)tileX, (uint8_t)row, 2, data);
  return true;
}

// ==================== I2C 初始化 ====================
void initTemperatureSensor() {
  // 新版 DHT20：7-bit I2C 0x38。
  if (probeI2C(0x38)) {
    dht20.begin();  // Grove Temperature And Humidity Sensor 2.0.2 返回 void。
    tempKind = TEMP_DHT20;
    tempOk = true;
    return;
  }

  // 旧版 DHT11：D3 单线。没有可探测的 I2C 地址，因此做一次真实读取确认。
  dht11.begin();
  delay(280);
  float data[2] = {0, 0};
  if (dht11.readTempAndHumidity(data) == 0 && !isnan(data[0]) && !isnan(data[1])) {
    tempKind = TEMP_DHT11;
    tempOk = true;
    tempHasReading = true;
    humidityRH = data[0];
    temperatureC = data[1];
    tempSeq++;
  }
}

bool tryInitPressureAt(uint8_t address) {
  if (!probeI2C(address)) return false;

  uint8_t splId = 0;
  uint8_t bmpId = 0;
  const bool gotSplId = readI2CRegister(address, 0x0D, splId);
  const bool gotBmpId = readI2CRegister(address, 0xD0, bmpId);

  // SPA06/SPL07-003 product ID = 0x11。
  if (gotSplId && splId == 0x11 && spl.begin(address, &Wire)) {
    pressureKind = PRESS_SPA06;
    pressureOk = true;
    pressureAddress = address;
    spl.setPressureConfig(SPL07_4HZ, SPL07_16SAMPLES);
    spl.setTemperatureConfig(SPL07_4HZ, SPL07_1SAMPLE);
    spl.setMode(SPL07_CONT_PRES_TEMP);
    return true;
  }

  // BMP280 chip ID = 0x58。
  // Grove - Barometer Sensor BMP280 1.0.1 的 init() 不接受地址参数，
  // 并固定使用库内默认地址 0x77。Grove Beginner Kit 旧版板载 BMP280 即为 0x77。
  if (gotBmpId && bmpId == 0x58 && address == 0x77 && bmp.init()) {
    pressureKind = PRESS_BMP280;
    pressureOk = true;
    pressureAddress = address;
    return true;
  }

  return false;
}

void initI2CDevices() {
  Wire.begin();
  Wire.setClock(100000);
  delay(20);

  initTemperatureSensor();

  // LIS3DHTR：Grove Beginner Kit 使用 0x19。
  if (probeI2C(0x19)) {
    LIS.begin(Wire, 0x19);
    delay(100);
    if (LIS) {
      accelOk = true;
      LIS.setOutputDataRate(LIS3DHTR_DATARATE_50HZ);
      LIS.setHighSolution(true);
    }
  }

  // 新旧气压传感器都常见于 0x77，另尝试 0x76。
  if (!tryInitPressureAt(0x77)) tryInitPressureAt(0x76);

  // OLED：官方 0x78 为 8-bit 表示法，对应 7-bit 0x3C。
  if (probeI2C(0x3C)) {
    oledOk = true;
    u8x8.setBusClock(100000);
    u8x8.begin();
    u8x8.setPowerSave(0);
    u8x8.setFlipMode(1);
    u8x8.setFont(u8x8_font_chroma48medium8_r);
    oledWriteText("MAKERSEED|TWIN V1.10.2");
  }

  Wire.setClock(100000);
}

// ==================== 传感器更新 ====================
void updateTemperature(unsigned long now) {
  if (!tempOk) return;
  const uint16_t interval = (tempKind == TEMP_DHT11) ? DHT11_INTERVAL_MS : DHT20_INTERVAL_MS;
  if ((unsigned long)(now - lastTempMs) < interval) return;
  lastTempMs = now;

  float data[2] = {0, 0};
  int result = -1;
  if (tempKind == TEMP_DHT20) result = dht20.readTempAndHumidity(data);
  else if (tempKind == TEMP_DHT11) result = dht11.readTempAndHumidity(data);

  if (result == 0 && !isnan(data[0]) && !isnan(data[1])) {
    humidityRH = data[0];
    temperatureC = data[1];
    tempHasReading = true;
    tempSeq++;
  }
}

void updatePressure(unsigned long now) {
  if (!pressureOk) return;
  if ((unsigned long)(now - lastPressureMs) < PRESS_INTERVAL_MS) return;
  lastPressureMs = now;

  if (pressureKind == PRESS_SPA06) {
    if (spl.pressureAvailable()) {
      const double pa = spl.readPressure();
      if (!isnan(pa) && pa > 10000.0 && pa < 120000.0) {
        pressureHpa = (float)(pa / 100.0);
        pressureHasReading = true;
        pressureSeq++;
      }
    }
  } else if (pressureKind == PRESS_BMP280) {
    const uint32_t pa = bmp.getPressure();
    if (pa > 10000UL && pa < 120000UL) {
      pressureHpa = (float)pa / 100.0f;
      pressureHasReading = true;
      pressureSeq++;
    }
  }
}

void updateAcceleration() {
  if (!accelOk) return;
  accelX = LIS.getAccelerationX();
  accelY = LIS.getAccelerationY();
  accelZ = LIS.getAccelerationZ();
}

// ==================== 协议上行 ====================
void sendHello() {
  Serial.print(F("{\"type\":\"hello\",\"protocol\":\"makerseed-twin\",\"version\":4,"));
  Serial.print(F("\"board\":\"Grove Beginner Kit / Seeeduino Lotus\",\"baud\":115200,"));
  Serial.print(F("\"capTemp\":")); Serial.print(tempOk ? 1 : 0);
  Serial.print(F(",\"capDht20\":")); Serial.print(tempKind == TEMP_DHT20 ? 1 : 0);
  Serial.print(F(",\"tempKind\":\"")); Serial.print(tempKindText()); Serial.print(F("\""));
  Serial.print(F(",\"capPressure\":")); Serial.print(pressureOk ? 1 : 0);
  Serial.print(F(",\"pressureKind\":\"")); Serial.print(pressureKindText()); Serial.print(F("\""));
  Serial.print(F(",\"pressureAddr\":")); Serial.print(pressureAddress);
  Serial.print(F(",\"capAccel\":")); Serial.print(accelOk ? 1 : 0);
  Serial.print(F(",\"capOled\":")); Serial.print(oledOk ? 1 : 0);
  Serial.println(F("}"));
}

void sendAckNumber(const __FlashStringHelper* command, long value) {
  Serial.print(F("{\"type\":\"ack\",\"cmd\":\""));
  Serial.print(command);
  Serial.print(F("\",\"value\":"));
  Serial.print(value);
  Serial.println(F("}"));
}

// OT ACK 明确包含 "seq"，网页用它确认每个 tile。
void sendAckWithSeq(const __FlashStringHelper* command, int16_t seq, long value) {
  Serial.print(F("{\"type\":\"ack\",\"cmd\":\""));
  Serial.print(command);
  Serial.print(F("\",\"seq\":"));
  Serial.print(seq);
  Serial.print(F(",\"value\":"));
  Serial.print(value);
  Serial.println(F("}"));
}

void printFloatOrNull(float value, bool valid, uint8_t digits) {
  if (valid && !isnan(value)) Serial.print(value, digits);
  else Serial.print(F("null"));
}

void sendState() {
  const uint16_t knob = analogRead(KNOB_ADC);
  const uint16_t light = analogRead(LIGHT_ADC);
  const uint16_t soundRaw = analogRead(SOUND_ADC);
  const uint16_t soundLevel = readSoundLevel();

  const int rawButton = digitalRead(BUTTON_PIN);
  const uint8_t buttonPressed = BUTTON_ACTIVE_HIGH
    ? (rawButton == HIGH ? 1 : 0)
    : (rawButton == LOW ? 1 : 0);

  updateAcceleration();

  Serial.print(F("{\"type\":\"state\",\"knob\":")); Serial.print(knob);
  Serial.print(F(",\"light\":")); Serial.print(light);
  Serial.print(F(",\"sound\":")); Serial.print(soundLevel);
  Serial.print(F(",\"soundRaw\":")); Serial.print(soundRaw);
  Serial.print(F(",\"button\":")); Serial.print(buttonPressed);
  Serial.print(F(",\"led\":")); Serial.print(ledState ? 1 : 0);
  Serial.print(F(",\"buzzer\":")); Serial.print(buzzerFrequency);

  Serial.print(F(",\"temp\":")); printFloatOrNull(temperatureC, tempHasReading, 2);
  Serial.print(F(",\"hum\":")); printFloatOrNull(humidityRH, tempHasReading, 2);
  Serial.print(F(",\"tempSeq\":")); Serial.print(tempSeq);

  Serial.print(F(",\"pressure\":")); printFloatOrNull(pressureHpa, pressureHasReading, 2);
  Serial.print(F(",\"pressureSeq\":")); Serial.print(pressureSeq);

  Serial.print(F(",\"ax\":")); printFloatOrNull(accelX, accelOk, 3);
  Serial.print(F(",\"ay\":")); printFloatOrNull(accelY, accelOk, 3);
  Serial.print(F(",\"az\":")); printFloatOrNull(accelZ, accelOk, 3);
  Serial.println(F("}"));
}

// ==================== 协议下行 ====================
void handleCommand(char* line) {
  if (strncmp(line, "LED ", 4) == 0) {
    setLed(atoi(line + 4) != 0);
    sendAckNumber(F("LED"), ledState ? 1 : 0);
    return;
  }

  if (strncmp(line, "BUZ ", 4) == 0) {
    long value = atol(line + 4);
    value = constrain(value, 0L, 5000L);
    setBuzzer((uint16_t)value);
    sendAckNumber(F("BUZ"), buzzerFrequency);
    return;
  }

  if (strncmp(line, "OLED ", 5) == 0) {
    oledTransferActive = false;
    oledWriteText(line + 5);
    sendAckNumber(F("OLED"), oledOk ? 1 : 0);
    return;
  }

  if (strcmp(line, "OBEGIN") == 0) {
    oledTransferActive = oledOk;
    if (oledOk) u8x8.clearDisplay();
    sendAckNumber(F("OBEGIN"), oledOk ? 1 : 0);
    return;
  }

  if (strncmp(line, "OT ", 3) == 0) {
    int16_t seq = -1;
    const bool ok = oledDrawTileCommand(line + 3, seq);
    sendAckWithSeq(F("OT"), seq, ok ? 1 : 0);
    return;
  }

  if (strcmp(line, "OEND") == 0) {
    const bool ok = oledOk && oledTransferActive;
    oledTransferActive = false;
    lastStateMs = millis();
    sendAckNumber(F("OEND"), ok ? 1 : 0);
    return;
  }

  if (strcmp(line, "OLEDCLR") == 0) {
    oledTransferActive = false;
    oledClear();
    lastStateMs = millis();
    sendAckNumber(F("OLEDCLR"), oledOk ? 1 : 0);
    return;
  }

  if (strcmp(line, "GET") == 0) {
    sendState();
    return;
  }

  if (strcmp(line, "HELLO") == 0) {
    sendHello();
    return;
  }

  if (strcmp(line, "PING") == 0) {
    Serial.println(F("{\"type\":\"pong\"}"));
    return;
  }

  Serial.println(F("{\"type\":\"error\",\"message\":\"unknown command\"}"));
}

void readSerialCommands() {
  while (Serial.available() > 0) {
    const char c = (char)Serial.read();
    if (c == '\r') continue;

    if (c == '\n') {
      if (commandLength > 0) {
        commandBuffer[commandLength] = '\0';
        handleCommand(commandBuffer);
        commandLength = 0;
      }
      continue;
    }

    if (commandLength < sizeof(commandBuffer) - 1) {
      commandBuffer[commandLength++] = c;
    } else {
      commandLength = 0;
      Serial.println(F("{\"type\":\"error\",\"message\":\"command too long\"}"));
    }
  }
}

// ==================== Arduino ====================
void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  setLed(false);
  setBuzzer(0);

  Serial.begin(SERIAL_BAUD);
  delay(120);

  initI2CDevices();
  sendHello();

  // 第一次有效读取尽快发生。
  lastTempMs = millis() - ((tempKind == TEMP_DHT11) ? DHT11_INTERVAL_MS : DHT20_INTERVAL_MS);
  lastPressureMs = millis() - PRESS_INTERVAL_MS;
  updateTemperature(millis());
  updatePressure(millis());
  sendState();
}

void loop() {
  readSerialCommands();

  const unsigned long now = millis();

  // OLED 位图传输期间暂停传感器 I2C 读取与 20 Hz 状态上报，
  // 让串口与 I2C 带宽只服务于当前 tile + ACK，避免 RX 缓冲挤压和总线争用。
  if (!oledTransferActive) {
    updateTemperature(now);
    updatePressure(now);

    if ((unsigned long)(now - lastStateMs) >= STATE_INTERVAL_MS) {
      lastStateMs = now;
      sendState();
    }
  }
}
