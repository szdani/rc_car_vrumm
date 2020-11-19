/*
 * Motor.c
 *
 *  Created on: Nov 15, 2020
 *      Author: dasz
 */


#include "Drivers/Motor.h"

void Motor_Init(struct MotorController *motorController, TIM_HandleTypeDef *motorPWM_Timer){
	motorController->motorPWM_Timer = motorPWM_Timer;
	HAL_TIM_IC_Start_IT(motorPWM_Timer, TIM_CHANNEL_1);
	Motor_Stop(motorController);
	return;
}

void Motor_Left(struct MotorController *motorController){
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_2);
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_3);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_1);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_4);
	return;
}

void Motor_Right(struct MotorController *motorController){
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_4);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_2);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_3);
	return;
}

void Motor_Forward(struct MotorController *motorController){
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_3);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_2);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_4);
	return;
}

void Motor_Backward(struct MotorController *motorController){
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_2);
	HAL_TIM_PWM_Start(motorController->motorPWM_Timer, TIM_CHANNEL_4);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_1);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_3);
	return;
}

void Motor_Stop(struct MotorController *motorController){
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_1);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_2);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_3);
	HAL_TIM_PWM_Stop(motorController->motorPWM_Timer, TIM_CHANNEL_4);
}
