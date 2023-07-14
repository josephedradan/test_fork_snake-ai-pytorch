import os
from typing import Sequence

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer

from constants import Action
from constants import TYPE_GAME_STATE


class LinearQNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.linear1: nn.Module = nn.Linear(input_size, hidden_size)
        self.linear2: nn.Module = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, learning_rate, gamma):
        self.learning_rate: float = learning_rate
        self.gamma: float = gamma
        self.model: nn.Module = model
        self.optimizer: Optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.loss_function: _Loss = nn.MSELoss()  # Loss function

    def train_step_input_multiple(self,
                                  np_ndarray_game_states: np.ndarray,
                                  sequence_action: Sequence[Action],
                                  sequence_reward: Sequence[int],
                                  np_ndarray_game_states_next: np.ndarray,
                                  sequence_bool_player_dead: Sequence[bool],
                                  ):

        torch_tensor_game_states = torch.tensor(np_ndarray_game_states, dtype=torch.float)
        torch_tensor_action = torch.tensor(sequence_action, dtype=torch.long)
        torch_tensor_reward = torch.tensor(sequence_reward, dtype=torch.float)
        torch_tensor_game_state_nexts = torch.tensor(np_ndarray_game_states_next, dtype=torch.float)

        self.train_step_train(
            torch_tensor_game_states,
            torch_tensor_action,
            torch_tensor_reward,
            torch_tensor_game_state_nexts,
            sequence_bool_player_dead
        )

    def train_step_train(self,
                         torch_tensor_game_states: torch.Tensor,
                         torch_tensor_action: torch.Tensor,
                         torch_tensor_reward: torch.Tensor,
                         torch_tensor_game_states_next: torch.Tensor,
                         sequence_bool_player_dead: Sequence[bool],
                         ):
        """

        :param torch_tensor_game_states:
        :param torch_tensor_action:
        :param torch_tensor_reward:
        :param torch_tensor_game_states_next:
        :param sequence_bool_player_dead:
        :return:
        """

        """
        1. Predicted Q values given current torch_tensor_game_states
        
        Notes:
            torch_tensor_actions_prediction shape is (n, 3) which is n rows 3 columns where each column
            corresponds to 
                (
                    Go forward direction relative to current direction, 
                    Go right relative to current direction, 
                    Go left relative to current direction
                )
        
        """
        torch_tensor_actions_prediction: torch.Tensor = self.model(torch_tensor_game_states)

        torch_tensor_actions_target = torch_tensor_actions_prediction.clone()
        """
        
        Notes:
            Bellman Equation:
                newQ(s, a) = Q(s, a) + alpha * (Reward(s, a) + gamma * max(q'(s', a')) - Q(s, a))
                
                s = game state
                a = action
                
                s' = future game state
                a' = future action 
                
                alpha = learning rate
                gamma = discount rate
            

            
        """

        for index in range(len(sequence_bool_player_dead)):
            q_new = torch_tensor_reward[index]

            # If player is not dead
            if not sequence_bool_player_dead[index]:
                """
                
                Notes:
                    Update Q
                        q_new(s, a) = Reward(s, a) + gamma * max(q'(s', a'))     
                        
                            s = game state
                            a = action
                            
                            q' = future quality value
                            s' = future game state
                            a' = future action 
                            
                            alpha = learning rate
                            gamma = discount rate
                    
                """
                q_new = (
                        torch_tensor_reward[index] +
                        self.gamma * torch.max(self.model(torch_tensor_game_states_next[index]))
                )

            torch_tensor_actions_target[index][torch.argmax(torch_tensor_action[index]).item()] = q_new

        # 2: q_new = r + y * max(next_predicted Q value) -> only do this if not sequence_bool_player_dead


        print("FFFFFFFFFFFFF")
        print(torch_tensor_actions_target)
        print(torch_tensor_actions_prediction)

        # torch_tensor_actions_prediction.clone()
        # preds[argmax(torch_tensor_action)] = q_new
        self.optimizer.zero_grad()  # Empty the gradiant

        loss = self.loss_function(torch_tensor_actions_target, torch_tensor_actions_prediction)
        loss.backward()  # Backpropagation
        self.optimizer.step()

    def train_step_input_single(self,
                                game_state: TYPE_GAME_STATE,
                                action: Action,
                                reward: int,
                                game_state_next: TYPE_GAME_STATE,
                                done: bool
                                ):

        print("TRAIN STEP IN")
        print("game_state", game_state)
        print("action", action)
        print("reward", reward)
        print("game_state_next", game_state_next)
        print("sequence_bool_player_dead", done)

        torch_tensor_game_state = torch.tensor(game_state, dtype=torch.float)
        torch_tensor_action = torch.tensor(action, dtype=torch.long)
        torch_tensor_reward = torch.tensor(reward, dtype=torch.float)
        torch_tensor_game_state_next = torch.tensor(game_state_next, dtype=torch.float)
        # (n, x)  # This is a shape

        print("TRAIN STEP AFTER")
        print("torch_tensor_game_state", torch_tensor_game_state.shape, torch_tensor_game_state)
        print("torch_tensor_action", torch_tensor_action.shape, torch_tensor_action)
        print("torch_tensor_reward", torch_tensor_reward.shape, torch_tensor_reward)
        print("torch_tensor_game_state_next", torch_tensor_game_state_next.shape, torch_tensor_game_state_next)
        print("done", done)

        # (1, x)  # This is a shape
        torch_tensor_game_states = torch.unsqueeze(torch_tensor_game_state, 0)
        torch_tensor_action = torch.unsqueeze(torch_tensor_action, 0)
        torch_tensor_reward = torch.unsqueeze(torch_tensor_reward, 0)
        torch_tensor_game_states_next = torch.unsqueeze(torch_tensor_game_state_next, 0)
        sequence_bool_player_dead = (done,)

        print("PAST LENGHT")
        print("torch_tensor_game_state", torch_tensor_game_states.shape, torch_tensor_game_states)
        print("torch_tensor_action", torch_tensor_action.shape, torch_tensor_action)
        print("torch_tensor_reward", torch_tensor_reward.shape, torch_tensor_reward)
        print("torch_tensor_game_state_next", torch_tensor_game_states_next.shape, torch_tensor_game_state_next)
        print("sequence_bool_player_dead", sequence_bool_player_dead)

        self.train_step_train(
            torch_tensor_game_states,
            torch_tensor_action,
            torch_tensor_reward,
            torch_tensor_game_states_next,
            sequence_bool_player_dead,
        )

        # print()
        # # 1: predicted Q values with current game_state_current
        # pred: torch.Tensor = self.model(torch_tensor_game_state)
        #
        # target = pred.clone()
        # for idx in range(len(sequence_bool_player_dead)):
        #     Q_new = torch_tensor_reward[idx]
        #     if not sequence_bool_player_dead[idx]:
        #         Q_new = torch_tensor_reward[idx] + self.gamma * torch.max(self.model(torch_tensor_game_state_next[idx]))
        #
        #     target[idx][torch.argmax(torch_tensor_action[idx]).item()] = Q_new
        #
        # # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not sequence_bool_player_dead
        # # pred.clone()
        # # preds[argmax(torch_tensor_action)] = Q_new
        # self.optimizer.zero_grad()  # Empty the gradiant
        # loss = self.loss_function(target, pred)
        # loss.backward()
        #
        # self.optimizer.step()
