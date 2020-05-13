/*
 * bluetooth.h
 *
 *  Created on: May 8, 2020
 *      Author: dasz
 */

#ifndef INC_MOTOR_H_
#define INC_MOTOR_H_

#include "main.h"
#include <string.h>

extern TIM_HandleTypeDef htim4;
extern TIM_HandleTypeDef htim1;

void motor_init();
void motor_stop();
void motor_left();
void motor_right();
void motor_forward();
void motor_backward();


#endif /* INC_BLUETOOTH_H_ */
