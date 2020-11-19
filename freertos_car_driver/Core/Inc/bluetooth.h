/*
 * bluetooth.h
 *
 *  Created on: Nov 14, 2020
 *      Author: szdani
 */

#ifndef INC_BLUETOOTH_H_
#define INC_BLUETOOTH_H_

#include <string.h>
#include "stm32f1xx_hal.h"

#define BT_TOPIC_DISTANCE_SENSOR "DIS"
#define BT_TOPIC_DEBUG "DEB"

#define BT_MSG_PING "PING"

struct Bluetooth {
	UART_HandleTypeDef *UARTHandler;
	char message_buffer[50];
	uint8_t timer_count;
	uint8_t buffer_index;
};

void BluetoothSetup(struct Bluetooth *bluetooth_uart, UART_HandleTypeDef *handler);
void BluetoothSendMessage(struct Bluetooth *bluetooth_uart, char topic[], char message[]);

uint8_t string_compare(char array1[], char array2[], uint16_t length);


#endif /* INC_BLUETOOTH_H_ */
