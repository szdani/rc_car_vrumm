/*
 * bluetooth.c
 *
 *  Created on: May 8, 2020
 *      Author: dasz
 */

#include "bluetooth.h"
#include "motor.h"

char buffer[50];
uint8_t timer_count = 0, buffer_index = 0;

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

void Message_handler()
{
	if(string_compare(buffer, "F_LEFT", strlen("F_LEFT"))){
		motor_left();
	}
	else if(string_compare(buffer, "F_RIGHT", strlen("F_RIGHT"))){
		motor_right();
	}
	else if(string_compare(buffer, "FORWARD", strlen("FORWARD"))){
		motor_forward();
	}
	else if(string_compare(buffer, "BACK", strlen("BACK"))){
		motor_backward();
	}
	else if(string_compare(buffer, "STOP", strlen("STOP"))){
		motor_stop();
		//HAL_UART_Transmit(&huart2, (uint8_t*)"STOP", strlen("STOP"), 500);
	}else{
		motor_stop();
		strcat(buffer, "\n");
		HAL_UART_Transmit(&huart2, (uint8_t*)buffer, strlen(buffer), 500);
	}

	memset(buffer, 0, sizeof(buffer));
	buffer_index = 0;
	timer_count = 0;
}
