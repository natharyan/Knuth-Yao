import random
from math import log2, ceil

P_X = [1/8, 1/4, 1/8, 1/4, 1/4]
Omega = [1, 2, 3, 4, 5]

class Node:
    def __init__(self, label):
        self.label = label
        self.height = 0
        self.left = None
        self.right = None

def buildTotalTree(root, height):
    if height == 0:
        root.left = None
        root.right = None
        return root
    root.left = buildTotalTree(Node('null'), height-1)
    root.right = buildTotalTree(Node('null'), height-1)
    return root

def printtree(node, level=0, prefix="Root: "):
    if node is not None:
        print(' ' * 4 * level + prefix + str(node.label))
        if node.left or node.right:
            if node.left:
                printtree(node.left, level + 1, "L--- ")
            if node.right:
                printtree(node.right, level + 1, "R--- ")

def dfs_label(root, height, idx, target_height, used_paths):
    if root is None:
        return False
    if height == target_height and root.label == 'null':
        current = root
        temp_root = root
        while current:
            if id(current) in used_paths:
                return False
            current = current.left if current.left and current.left.label != 'null' else current.right
        root.label = str(Omega[idx])
        root.left = None
        root.right = None
        while temp_root:
            used_paths.add(id(temp_root))
            temp_root = temp_root.left if temp_root.left else temp_root.right
        return True
    if height < target_height:
        if dfs_label(root.left, height + 1, idx, target_height, used_paths):
            return True
        if dfs_label(root.right, height + 1, idx, target_height, used_paths):
            return True
    return False

def addLabels(root, heights):
    idx_by_height = [(i, heights[i]) for i in range(len(heights))]
    idx_by_height.sort(key=lambda x: x[1], reverse=True)
    used_paths = set()
    for idx, height in idx_by_height:
        target_height = int(ceil(height))
        dfs_label(root, 0, idx, target_height, used_paths)
    return root

def simulatePx(root, height=0):
    if root.left is None and root.right is None:
        return root.label, ''
    
    cointflip = random.randint(0, 1)
    if cointflip == 0:
        output, codeword = simulatePx(root.left, height+1)
        codeword = '0' + codeword
    else:
        output, codeword = simulatePx(root.right, height+1)
        codeword = '1' + codeword
    
    return int(output), codeword

if __name__ == '__main__':
    print("Height of each label:")
    heights = [int(log2(1/p)) for p in P_X]
    print(heights)
    root = Node('null')
    depth = int(log2(1/min(P_X)))
    print("\nDepth of the tree:",depth)
    root = buildTotalTree(root, height=depth)
    print("\nEmpty tree constructed:")
    printtree(root)
    root = addLabels(root, heights)
    print("\nLabels added:")
    printtree(root)

    print("\nSimulation of P_X using a fair coin flip and the total tree:")
    a_i = {}
    for i in range(len(Omega)):
        a_i[Omega[i]] = 0
    num_simulations = 200
    labels = []
    for i in range(num_simulations):
        simulationoutput = simulatePx(root)
        a_i[simulationoutput[0]] += 1
        print(f"(label: {simulationoutput[0]}, probability: {P_X[Omega.index(int(simulationoutput[0]))]})",end=", ")
        labels.append((simulationoutput[0],simulationoutput[1]))
    print("\nLabel counts:")
    print(a_i)

    print("\nSample probabilities:")
    tot_count = sum(a_i.values())
    samp_probs = {}
    for key in a_i:
        samp_probs[key] = a_i[key]/tot_count
    print(samp_probs)
    print("\nSource probabilities:")
    sourceprobs = {}
    for idx,x in enumerate(Omega):
        sourceprobs[x] = P_X[idx]
    print(sourceprobs)
    print("\nC:")
    print(set(labels))
    print("\nCodewords:")
    for i in range(num_simulations):
        print(labels[i],end=", ")
    print("\nAverage length of the code:")
    avg_length = 0
    for lab_px in samp_probs:
        avg_length += samp_probs[lab_px]*log2(1/samp_probs[lab_px])
    print(avg_length)
    print("\nEntropy of the source:")
    entropy = 0
    for p in P_X:
        entropy += p*log2(1/p)
    print(entropy)
