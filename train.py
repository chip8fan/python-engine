import torch
from torch import nn
from torch import optim
from sklearn.model_selection import train_test_split
import sys
import os
device = torch.device("mps")
for file in os.listdir(f"{os.getcwd()}/{sys.argv[1]}"):
    f = open(f"{sys.argv[1]}/{file}")
    lines = [l.strip() for l in f]
    f.close()
    X = torch.tensor(eval(lines[0]), dtype=torch.float).to(device)
    X = X.view(X.shape[0], -1)
    y = torch.tensor(eval(lines[1]), dtype=torch.float).to(device)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25)
    if os.path.isfile('model.pth'):
        model = torch.load('model.pth', weights_only=False).to(device)
    else:
        input_layers = 768
        hidden_layers = 1
        output_layers = 1
        model = nn.Sequential(
            nn.Linear(input_layers, hidden_layers),
            nn.LeakyReLU(),
            nn.Linear(hidden_layers, output_layers)
        ).to(device) # input layer size x, hidden layer size x, output layer size x
    loss = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    old_training_loss = sys.maxsize
    old_testing_loss = sys.maxsize
    epoch = 1
    while True:
        model.train()
        predictions = model(X_train)
        MSE = loss(predictions, y_train)
        MSE.backward()
        old_training_loss = MSE
        optimizer.step()
        optimizer.zero_grad()
        model.eval()
        with torch.no_grad():
            test_predictions = model(X_test)
            test_MSE = loss(test_predictions, y_test)
        if test_MSE > old_testing_loss or test_MSE == 0:
            break
        old_testing_loss = test_MSE
        print(f"Epoch {epoch} | Training Loss: {MSE} | Validation Loss: {test_MSE}")
        epoch += 1
    torch.save(model, 'model.pth')