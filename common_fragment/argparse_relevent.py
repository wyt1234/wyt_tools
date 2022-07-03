import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Hyperparameters Setting for PPO-continuous")
    parser.add_argument("--use_tanh", type=float, default=True, help="Trick 10: tanh activation function")
    args = parser.parse_args()