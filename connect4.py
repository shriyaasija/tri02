import numpy as np
import pygame 
import math 
import sys

blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)

player = 0
bonita = 1

empty = 0
player_piece = 1
bonita_piece = 2

row_count = 7
column_count = 6
even = 0 
odd = 1

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(bpard, row, col, piece):
    board[row][column] = piece 

def is_valid_location(board, col):
    return  board[row_count-1][col] == 0

def next_open_row(board, col):
    for i in range(row_count):
        if board[i][col] == 0:
            return i

def print_board(board):
    print(np.flip(board,0))

def winning_condition(board, piece):

    #horizontal win
    for c in range(column_count-3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece:
                return True

    # vertical win
    for c in range(column_count):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece:
                return True

    #positive diagonal win
    for c in range(column_count-3):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece:
                return True

    #negative diagonal win
    for c in range(column_count-3):
        for r in range(3,row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece:
                return True

def evaluate_board(window, piece):
    score = 0
