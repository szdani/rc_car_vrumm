/*
 * motor.c
 *
 *  Created on: May 13, 2020
 *      Author: dasz
 */


#include "motor.h"


void motor_stop_safety_IT(){
	HAL_TIM_Base_Stop_IT(&htim4);
	__HAL_TIM_SET_COUNTER(&htim4, 0);
	HAL_TIM_Base_Start_IT(&htim4);
}

void motor_start_safety_IT(){
	HAL_TIM_Base_Start_IT(&htim4);
}

void motor_stop(){
	// Turn off LEDs
	HAL_GPIO_WritePin(GPIOD, LD5_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOD, LD4_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOD, LD3_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOD, LD6_Pin, GPIO_PIN_SET); // TODO RESET
	// Turn off PWM signal for motor control
	HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_1);
	HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_2);
}


void motor_left(){
	// Stop safety IT
	motor_stop_safety_IT();
	// Reset state - stop leds and motors
	motor_stop();
	// Left turn
	HAL_GPIO_WritePin(GPIOD, LD4_Pin, GPIO_PIN_SET);
	HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
	// Restart safety timer
	motor_start_safety_IT();
}

void motor_right(){
	// Stop safety IT
	motor_stop_safety_IT();
	// Reset state - stop leds and motors
	motor_stop();
	// Right turn
	HAL_GPIO_WritePin(GPIOD, LD5_Pin, GPIO_PIN_SET);
	HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
	// Restart safety timer
	motor_start_safety_IT();
}

void motor_forward(){
	// Stop safety IT
	motor_stop_safety_IT();
	// Reset state - stop leds and motors
	motor_stop();
	// Move forward
	HAL_GPIO_WritePin(GPIOD, LD3_Pin, GPIO_PIN_SET);
	HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
	HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
	// Restart safety timer
	motor_start_safety_IT();
}

void motor_backward(){
	// Stop safety IT
	motor_stop_safety_IT();
	// Reset state - stop leds and motors
	motor_stop();
	// Move forward
	HAL_GPIO_WritePin(GPIOD, LD6_Pin, GPIO_PIN_SET);
	// TODO bck power - GPIO + HW
	// Restart safety timer
	motor_start_safety_IT();
}
