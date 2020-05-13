/*
 * bluetooth.h
 *
 *  Created on: May 8, 2020
 *      Author: dasz
 */

#ifndef INC_BLUETOOTH_H_
#define INC_BLUETOOTH_H_

#include "main.h"
#include <string.h>

extern char buffer[50];
extern uint8_t timer_count, buffer_index;
extern UART_HandleTypeDef huart2;
extern TIM_HandleTypeDef htim1;

uint8_t string_compare(char array1[], char array2[], uint16_t length);
void Message_handler();


#endif /* INC_BLUETOOTH_H_ */
