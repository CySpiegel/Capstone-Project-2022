
#return a dictionary of actions available
def dictActions(input_nodes, context):
    context['inform'] = 'unknown'
    actions = {}
    for node in input_nodes:
        nodeAction = node.execute(context)
        actions[nodeAction] = node
    context['inform'] = 'known'
    return actions

# Perform the nodes action based on context
def performAction(actions, action, context):
    if action in actions:
        return actions[action].execute(context)
    else:
        return throwError(1)


def throwError(error):
    errorTable = {}
    errorTable[1] = "The current action from context is not found in the dictionary of actions provided. \
    Please check that leaf nodes are being generatted correctly. Most common issue is the leaf was not generated." 
    





    print(errorTable[error])
    return errorTable[error]