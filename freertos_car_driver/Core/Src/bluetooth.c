/*
 * bluetooth.h
 *
 *  Created on: Nov 14, 2020
 *      Author: szdani
 */

#include "bluetooth.h"

void BluetoothSetup(struct Bluetooth *bluetooth_uart, UART_HandleTypeDef *handler){
	bluetooth_uart->UARTHandler = handler;
	memset(bluetooth_uart->message_buffer, 0, sizeof(bluetooth_uart->message_buffer));
	bluetooth_uart->timer_count = 0;
	bluetooth_uart->buffer_index = 0;
	__HAL_UART_ENABLE_IT(bluetooth_uart->UARTHandler, UART_IT_RXNE);
	bluetooth_uart->buffer_index = 0;
}

void BluetoothSendMessage(struct Bluetooth *bluetooth_uart, char topic[], char message[]){
	char final_message[32];
	sprintf(final_message, "[%s:%s]", topic, message);
	HAL_UART_Transmit(bluetooth_uart->UARTHandler, (uint8_t*)final_message, strlen(final_message), 50);
}

uint8_t string_compare(char array1[], char array2[], uint16_t length)
{
	 uint8_t comVAR=0, i;
	 for(i=0;i<length;i++)
	   	{
	   		  if(array1[i]==array2[i])
	   	  		  comVAR++;
	   	  	  else comVAR=0;
	   	}
	 if (comVAR==length)
		 	return 1;
	 else 	return 0;
}
