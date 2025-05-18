import torch
from torch import nn


inputData = torch.tensor([
    [-20.0, 15.0, 1.0],
    [-15.0, 10.0, 2.0],
    [-10.0, 12.0, 0.5],
    [-5.0, 10.0, 1.0],
    [0.0, 8.0, 2.0],
    [2.0, 5.0, 1.0],
    [5.0, 7.0, 0.0],
    [8.0, 5.0, 0.0],
    [10.0, 3.0, 0.0],
    [12.0, 2.0, 0.0],
    [15.0, 4.0, 0.0],
    [18.0, 3.0, 0.0],
    [20.0, 2.0, 0.0],
    [22.0, 1.0, 0.0],
    [25.0, 2.0, 0.0],
    [27.0, 3.0, 0.0],
    [30.0, 1.0, 0.0],
    [32.0, 2.0, 0.0],
    [35.0, 1.0, 0.0],
    [38.0, 3.0, 0.0],
    [10.0, 12.0, 2.0],
    [15.0, 15.0, 3.0],
    [20.0, 10.0, 4.0],
    [25.0, 12.0, 5.0],
    [28.0, 15.0, 5.0],
])

result = torch.tensor([
    [0.0],   # очень холодно, сильный ветер, зима
    [0.2],   # мороз + осадки
    [0.7],   # просто мороз
    [1.0],   # -5, сильный ветер
    [1.5],   # около 0, дождь
    [2.0],   # прохладно
    [2.5],   # всё ещё куртка
    [3.0],   # уже весна
    [3.5],   # прохладно, но комфортно
    [4.0],   # легкая одежда
    [5.0],   # рубашка/кофта
    [6.0],   # майка/футболка
    [6.5],   # лето
    [7.0],   # лето
    [8.0],   # тепло
    [8.5],   # тепло, комфортно
    [9.0],   # жара
    [9.2],   # ещё жарче
    [9.7],   # почти максимум
    [10.0],  # максимальная жара, минимум одежды
    [3.0],   # тёплая погода, но ветер и осадки
    [3.5],   # весна, но сильный ветер и дождь
    [5.0],   # тёплая, но ветреная
    [6.0],   # жарко, но осадки и ветер
    [6.5],   # жарко, но неприятные условия
])



print(inputData.shape)
print(result.shape)

class SimpleNeuron(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(3, 8),
            nn.LeakyReLU(),
            nn.Linear(8, 4),
            nn.LeakyReLU(),
            nn.Linear(4, 1)  # Выход — одно число
        )

    def forward(self, inputD):
        return self.model(inputD)


def load_model():
    try:
        _loadmodel = SimpleNeuron()
        _loadmodel.load_state_dict(torch.load("AImodel/model.pth"))
        _loadmodel.eval()
        return _loadmodel

    except Exception as e:
        print("[ERROR LOAD]", e)
        return SimpleNeuron()

model = load_model()
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

def _learn():
    for epoch in range(4000):
        optimizer.zero_grad()
        output = model(inputData)
        loss = criterion(output, result)

        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print("[LOSS]", loss.item())

    torch.save(model.state_dict(), "AImodel/model.pth")
    print("Finished Saved")

def _test():
    print("test")
    DataTest1 = input()
    DataTest2 = input()
    DataTest3 = input()
    inputData = torch.tensor([[float(DataTest1), float(DataTest2), float(DataTest3)]])
    print(model(inputData))


def request(temp: str, veter: str, osadky: str):
    inputData = torch.tensor([[float(temp), float(veter), float(osadky)]])
    return model(inputData)

_test()