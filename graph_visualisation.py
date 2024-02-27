import graphviz

def draw_decision_tree():
    dot = graphviz.Digraph(comment='Dual-Step Growth Note')

    # Define nodes
    dot.node('A', 'Start\nInitial Investment $10,000')
    dot.node('B', 'Index <= -20%?\nCapital Protection Threshold')
    dot.node('C', 'Principal Reduction\nProportional to >20% loss')
    dot.node('D', 'Index > -20%')
    dot.node('E', 'Index Rise')
    dot.node('F', 'Participation in Upside\n50% of Index Gain, up to 20% Cap')
    dot.node('G', 'No Participation\nPrincipal Returned')

    # Define edges
    dot.edges(['AB', 'BD'])
    dot.edge('B', 'C', label='Yes')
    dot.edge('B', 'D', label='No')
    dot.edge('D', 'E', label='Index Rises')
    dot.edge('E', 'F', label='Calculate Gain')
    dot.edge('D', 'G', label='Index Does Not Rise')

    # Save the diagram to a file in the current working directory
    filename = 'dual_step_growth_note_decision_tree'
    dot.render(filename, format='png', cleanup=True)

    # Return the path to the generated image
    return f'{filename}.png'

# Execute the function and get the path to the generated image
tree_image_path = draw_decision_tree()
print(f'Decision tree image saved at: {tree_image_path}')
