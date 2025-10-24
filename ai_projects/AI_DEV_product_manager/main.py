import model.models as models
import app.app as app
import torch
import os
import sys
import random as rand
import torch.nn as nn

max_input = 9
max_output = 160

model = models.ModelV5(max_input, max_output)

def save_model():
    global model
    torch.save(model.state_dict(), "saved/model.pt")

def load_model():
    global model
    model.load_state_dict(torch.load("saved/model.pt"))

def clear_screen():
    if os.name == "posix":
        os.system("clear")  
    else:
        os.system("cls")

def train():
    epochs = 15000
    
    batch_size = 32
    random_choice = 0.2
    random_degrate = 0.005
    
    
    all_loss = 0
    failed = 0
    success = 0
    
    step = torch.optim.lr_scheduler.StepLR(model.optimizer, 5000, gamma=0.9)
    for epoch in range(epochs):
        clear_screen()
        print(f"Epoch: {epoch}")
        
        
        samples = []
        means = []
        expiry_times = []
        left_overs = []
        for _ in range(batch_size):
            sample = app.get_random_sales()
            mean = sum(sample) / len(sample)
            expiry_time = app.get_random_expiry_time()
            
            
            
            left_over = app.get_random_product_size(expiry_time*mean * 0.5)
            
            # print(f"left over: {left_over}")
            
            left_overs.append(left_over)
            expiry_times.append(expiry_time)
            samples.append(sample + [expiry_time] + [left_over])
            means.append(mean)
        
        

        
        output: torch.Tensor = model(app.make_usable_input_norml(samples))
        
        choices = output.argmax(dim=1)
        print(app.make_usable_input_norml(samples),"\n", choices, "\n", output)
        
        rewards = []
        
        for pos, choice in enumerate(choices):
            reward = 0
            if rand.randint(1, 100) < (random_choice * 100) and random_choice > 0.0:
                choice = torch.tensor(rand.randint(0, max_output), dtype=torch.float)
                random_choice -= random_degrate
            order = app.order_amount * (choice)
            print("###############")
            print(f"left over: {left_overs[pos]}")
            print(f"order: {order}")
            product_size = left_overs[pos] + order
            
            days = product_size / means[pos]
            print(f"product size: {product_size}")
            print(f"mean: {means[pos]}")
            print(f"expiry time: {expiry_times[pos]}")
            print(f"days lasted: {days}")
            
            if days > expiry_times[pos]*0.5 and days < expiry_times[pos]:
                number = abs((expiry_times[pos]*0.5 + expiry_times[pos])/2 - days) if abs((expiry_times[pos]*0.5 + expiry_times[pos])/2 - days) != 0 else 0.5
                reward += (((expiry_times[pos] - expiry_times[pos]*0.5)/2) / abs((expiry_times[pos]*0.5 + expiry_times[pos])/2 - days)  )
            else:
                reward -= 1 * abs((expiry_times[pos]*0.5 + expiry_times[pos])/2 - days)
            
            if reward <= 0:
                failed += 1
            else:
                success += 1
            
            print(f"reward: {reward}")
            # print(f"rewarded: {reward}")
            rewards.append(reward)

            print(f"success: {success} failed: {failed}")
            print(f"success rate: {round(success/(failed + success)*100, 1)}%")
        rewards = torch.tensor(rewards, dtype=torch.float32)

        # Replace any inf/nan first
        rewards = torch.nan_to_num(rewards, nan=0.0, posinf=0.0, neginf=0.0)

        # Compute std safely
        std = rewards.std()
        if std < 1e-6:  # too small to safely divide
            rewards = rewards - rewards.mean()
        else:
            rewards = (rewards - rewards.mean()) / (std + 1e-8)

        
        target = output.clone()
        target[torch.arange(batch_size), choices] = rewards
        
        loss = model.smoothl1loss(output, target)
        all_loss += loss.item()
        
        # logits = model(app.make_usable_input_norml(samples))
        # probs = torch.softmax(logits, dim=1)
        # log_probs = torch.log(probs[torch.arange(batch_size), choices])
        # loss = -(log_probs * rewards).mean()
        
        # print(f"Loss: {loss.item()}")
        # print(f"overall loss: {all_loss / (epoch+1)}")
        
        model.optimizer.zero_grad()
        loss.backward()
        model.optimizer.step()
        
        step.step()
        
        
        
        
    save_model()

def use():
    while True:
        try:
            numbers = list(map(float, input(f"input: last week sales, expiry time, left over: \n").split(" ")))
        except:
            print("invalid input")
            sys.exit()
        t_sales = torch.tensor(numbers[:-2], dtype=torch.float32)
        t_numbers = torch.tensor(numbers, dtype=torch.float32)
        amount_ordered = model(t_numbers).argmax().item() * app.order_amount
        mean = t_sales.mean().item()
        expiry_time = t_numbers[-2].item()
        days_lasted = (amount_ordered + t_numbers[-1].item()) / mean
        print(f"amount ordered: {amount_ordered}")
        print(f"mean: {mean}")
        print(f"days lasted: {days_lasted}")
        print(f"expiry time: {expiry_time}")
        
        
if __name__ == "__main__":
    clear_screen()
    print("Load a model? (y/n) (enter for no)")
    ans = load_model() if input() == "y" else None
    
    clear_screen()
    
    if input("Train a model? (y/n) (enter for no)\n") == "y":
        
        train()
    else:
        clear_screen()
        use()
    
    
    
    
    
    
    