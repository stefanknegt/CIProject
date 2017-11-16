population = 100
fitnesses = np.zeros(100)
terminate = False
while terminate == False:
    for i in range(0,population):
        name = "evolutionary_"+str(i)
        model = load_model()
        
    fitnesses[i] = test(model)
  death_idx = fitness.argsort()[:birth]
  parent_pool = fitness.argsort()[parents:]
  for i in death_idx:
    parent = np.random.choice(parents, 1, replace=False)
    parent_model = load_model(parent)
    model = mutate_model(parent_model)
