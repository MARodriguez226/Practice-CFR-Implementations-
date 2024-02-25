from tqdm import tqdm
import eval7
import numpy as np
import pickle
Rank = "2346789TJKQA"
Suits = "shdc"

with open("marco_abstraction/output_files/pickle_files/computed_distances.pickle",'rb') as hand_dict_file:
    hand_dict = pickle.load(hand_dict_file)

with open("marco_abstraction/output_files/pickle_files/computed_distances_canon.pickle",'rb') as canon_dict_file:
    canon_dict = pickle.load(canon_dict_file)

def initializeCenters(points,k):
    """
    points = [tuple(float)]
    centers for each hand
    """
    centroids = []
    centroid = points[np.random.randint(len(points))]
    centroids.append(centroid)

    for _ in tqdm(range(1,k)):
        distances = np.array([min(np.linalg.norm(point - np.array(centroid)) for centroid in centroids) for point in points])
        prob = distances/distances.sum()
        centroid = points[np.random.choice(len(points),p = prob)]
        centroids.append(centroid)

    return centroids

center_dict = {}
for hand in hand_dict:
    centers = initializeCenters(hand_dict[hand],4)
    center_dict[hand] = centers
# hand in str form: [centers]

with open("marco_abstraction/output_files/pickle_files/computed_centers.pickle",'wb') as center_pickled:
    pickle.dump(center_dict,center_pickled)

with open("marco_abstraction/output_files/computed_centers.txt",'a') as comp_cent:
    for center in center_dict:
        print(center,file = comp_cent)
        print(center_dict[center],file = comp_cent)
    print(center_dict,file = comp_cent)