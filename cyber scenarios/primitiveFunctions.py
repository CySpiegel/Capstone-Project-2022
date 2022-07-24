
def actions(input_nodes, context):
    action = context['action']
    context['inform'] = "unknown"
    actions = {}

    for node in input_nodes:
        nodeAction = node.execute(context)
        actions[nodeAction] = node

    #if check needed to see is action is in dict
    if action in actions:
        actions[action].execute(context)
    else:
        print("The current action from context is dictionary of actions")