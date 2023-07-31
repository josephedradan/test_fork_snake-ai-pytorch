# Deep Q Learning explained 
    
    Game
        Game asks PlayerAI to give an Action
        Game gives DataGame to PlayerAI
            PlayerAI
                PlayerAI gives DataGame to GeneratorGameState to generate GameState for specific DeepQLearningModel
                    GeneratorGameState
                        GeneratorGameState returns GameState
                PlayerAI gives GameState to AgentDeepQLearning
                    AgentDeepQLearning
                        Condition 1
                            AgentDeepQLearning returns random Tuple Action 
                        Condition 2
                            AgentDeepQLearning converts GameState to Tensor GameState
                            AgentDeepQLearning gives Tensor GameState shape (1, 3) to DeepQLearningModel
                                DeepQLearningModel
                                    DeepQLearningModel returns Tensor shape (1, 3) Action Prediction
                            AgentDeepQLearning converts Tensor Action Prediction to Tuple Action 
                            AgentDeepQLearning returns Tuple Action                    
                PlayerAI converts Tuple Action to Action
                PlayerAI returns Action
    Game
        Game handles PlayerAI's Action
        Game gives DataGame and DataPlayStepResult to PlayerAI
            PlayerAI
                PlayerAI gives DataGame to GeneratorGameState to generate GameState for specific DeepQLearningModel
                    GeneratorGameState returns GameState
                PlayerAI names GameState to GameState New
                PlayerAI extracts important data from DataPlayStepResult into Reward and Bool Dead
                PlayerAI gives GameState, Action, Reward, Bool Dead, GameState New to AgentDeepQLearning for training short term memory
                    AgentDeepQLearning
                        AgentDeepQLearning give GameState, Action, Reward, Bool Dead, GameState New to TrainerDeepQLearning for training short term memory
                            TrainerDeepQLearning
                                TrainerDeepQLearning converts GameState, Action, Reward, GameState New to their Tensor representations containg multiple of their kind
                                TrainerDeepQLearning converts Bool Dead into Tuple Bool Dead
                                TrainerDeepQLearning gives Tensor GameState shape (n, 3) to DeepQLearningModel
                                    DeepQLearningModel
                                        DeepQLearningModel returns Tensor shape (n, 3) Action Prediction
                                        DeepQLearningModel copies Tensor shape (n, 3) Action Prediction into Tensor shape (n, 3) Action Target
                                        DeepQLearningModel Will
                                            Loop over Tuple Bool Dead
                                                G
                                                If Bool Dead is False
                                                    
                    
# On the subject of playing as a food or a wall

    Problem:
        player_ai_q_learning requires a GeneratorGameStateFoodSingle which requires a method
        called get_chunk_first which only exists on a ContainerChunkSnake which does not exists on
        a ContainerChunk
        
        IF I WANT OT BE A FOOD THEN I WANT TO BE A FOOD