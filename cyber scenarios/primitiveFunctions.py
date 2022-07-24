
#return a dictionary of actions available
def dictActions(input_nodes, context):
    # set inform to unknown to force node type return
    context['inform'] = "unknown"
    
    # Build a dictionary of possible actions from input_nodes
    actions = {}
    for node in input_nodes:
        nodeAction = node.execute(context)
        actions[nodeAction] = node
    context['inform'] = "known"
    return actions

# Perform the nodes action based on context
def performAction(actions, action, context):
    if action in actions:
        return actions[action]
    else:
        print("The current action from context is dictionary of actions")
    