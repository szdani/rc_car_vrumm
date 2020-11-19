/*
 * Motor.h
 *
 *  Created on: Nov 15, 2020
 *      Author: Daniel
 */

#ifndef INC_DRIVERS_MOTOR_H_
#define INC_DRIVERS_MOTOR_H_

#include "stm32f1xx_hal.h"

#define MOTOR_STATUS_STOP 0
#define MOTOR_STATUS_FORWARD 1
#define MOTOR_STATUS_BACKWARD 2
#define MOTOR_STATUS_LEFT 3
#define MOTOR_STATUS_RIGHT 4

struct MotorController{
	uint8_t status;

	TIM_HandleTypeDef *motorPWM_Timer;
};

void Motor_Init(struct MotorController *motorController, TIM_HandleTypeDef *motorPWM_Timer);

void Motor_Left(struct MotorController *motorController);
void Motor_Right(struct MotorController *motorController);
void Motor_Forward(struct MotorController *motorController);
void Motor_Backward(struct MotorController *motorController);
void Motor_Stop(struct MotorController *motorController);


#endif /* INC_DRIVERS_MOTOR_H_ */
