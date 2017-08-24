"""query types are categorized as ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
as a list of keywords for querying 4 different research engines. """
import copy

import  CODE.filter_queues as filter_queues

QUERY_TYPES = ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
ENTITIES_NUM = 3
ENTITIES_LIST = ["RN", "U", "Y"]
STATE_SIZE = 4* ENTITIES_NUM
ACTIONS = ["query", "AcceptRN", "AcceptU", "AcceptY", "AcceptALL", "STOP"]
EMPTY_ENTITIES_CONFIDENCE_SCORE = {'RN': {'entity': [], 'confidenceScore': []}, 'U': {'entity': [], 'confidenceScore': []}, 'Y': {'entity': [], 'confidenceScore': []}}

#Environment for each episode (person_id)
class Environment:
    def __init__(self, person_id):
        self.person_id = str(person_id)
        self.path = "../DATA/entities_db/"+ self.person_id + '/queue_'

        #save extracted entities from queries in queues
        t = filter_queues.queires_to_queue(self.person_id)
        #list of queues inclusing the entities indexes in ../DATA/entities_db/person_id folder
        #indexes of queues_list come from  QUERY_TYPES = ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
        self.queues_list = t.filter_queues_save_indexes()
        self.originalEntities = t.originalEntities
        #self.BestEntities_Bestscores = {'RN': {'entity': [], 'confidenceScore': []}, 'U': {'entity': [['Epic', 'Willow']], 'confidenceScore': [0.5]}, 'Y': {'entity': [], 'confidenceScore': []}}

        self.query = 0 #query type
        self.currentEntities = self.queues_list[self.query].get()
        self.BestEntities_BestConfidence = self.currentEntities

        self.state = [0.0 for i in range(STATE_SIZE)]
        self.terminal = False

    #several various methods for selecting the best entities after each reconcilation
    #*********************************
    def majorityVote(self):
        pass

    def confidentVote(self, currEntities, NewEntities):
        print ('currEntities', currEntities)
        print('NewEntities',NewEntities)

        entities = []
        scores = []

        for ent in ENTITIES_LIST:
            entities.append(elem for elem in currEntities[ent]['entity'])
            entities.append(elem for elem in NewEntities[ent]['entity'])

            scores.append(elem for elem in currEntities[ent]['confidenceScore'])
            scores.append(elem for elem in NewEntities[ent]['confidenceScore'])

            print('entities', entities)
            print('scores',scores)

            entities = []
            scores = []

        pass
    #*********************************

    def check_match(self, entity, original_entities):
        # if original entity is None in scholarship.json DB
        if original_entities == None:
            return False

        for i in range(len(entity)):
            _element = ' '.join(entity[i])
            if str(_element).lower() == str(original_entities).lower():
                return True

        return False

    # updatining the state it should be based on the decision from DQN
    # but we make it randomly at this phase TODO updatign states should be modified based on the DQN agent decision
    def updateState(self, currEntities, newEntities):

        state_index = 0
        for value in currEntities.values():
            self.state[state_index] = value['confidenceScore']
            state_index += 1

        for value in newEntities.values():
            self.state[state_index] = value['confidenceScore']
            state_index += 1

        for ent in ENTITIES_LIST:
            if self.check_match(currEntities[ent]['entity'], self.originalEntities[ent]):
                self.state[state_index] = 1
            else:
                self.state[state_index] = 0
            state_index += 1

        for ent in ENTITIES_LIST:
            if self.check_match(newEntities[ent]['entity'], self.originalEntities):
                self.state[state_index] = 1
            else:
                self.state[state_index] = 0
            state_index += 1

        return

    #TODO QUICK : change reconcile
    def reconcileStates(self, currentEntities, newEntities, action):
        #print('currentEntities', currentEntities)
        #print('newEntities', newEntities)

        mergeEntities = currentEntities
        if action == ACTIONS[1]:
            mergeEntities["RN"] = newEntities["RN"]

        elif action == ACTIONS[2]:
            mergeEntities["U"] = newEntities["U"]

        elif action == ACTIONS[3]:
            mergeEntities["Y"] = newEntities["Y"]

        else:
            mergeEntities = newEntities

        return mergeEntities

    #TODO I may change the equality check later
    #this function checks if two entities are equal or not
    def checkEquality(self, original_entit, entit):
        """
        this function checks if the original entity is included in the extracted entity list
        :param original_entit:
        :param entit:
        :return:  if it finds the exact entity, it returns TRUE and the selected entity from entities list. This is because
        the coe extracts more than one entities from each article.
        """

        # if original entity is None in scholarship.json DB
        if original_entit == None:
            return False, None

        tempo_element = entit['entity']
        for i in range(len(entit['entity'])):
            _element = ' '.join(tempo_element[i])
            if str(_element).lower() == str(original_entit).lower():
                return True, {'entity':[tempo_element[i]], 'confidenceScore':[entit['confidenceScore'][i]]}

        return False, None

    def ComputeReward(self, currentEntities, prevEntities):

        #each correct entity has 0.33 value
        reward_unit = 1.0/ENTITIES_NUM
        goldEntites = self.originalEntities

        sum_reward = 0
        for entity in ENTITIES_LIST:
            check_result_current = self.checkEquality(goldEntites[entity], currentEntities[entity])
            check_result_prev = self.checkEquality(goldEntites[entity], prevEntities[entity])
            if(check_result_current[0]):
                sum_reward += reward_unit
                currentEntities[entity] = check_result_current[1]
            if(check_result_prev[0]):
                sum_reward -= reward_unit

        print(sum_reward, currentEntities)
        return sum_reward, currentEntities

    #TODO in the origninal paper, the agent select two options query or reconcilation every time but here I separated queries
    # like another action until now.
    # take a single step in the episod
    def step(self, action):
        if action == "query":
            self.query = (self.query + 1) % len(QUERY_TYPES)

        elif action != "STOP":
            prevEntities = copy.copy(self.currentEntities)
            newEntities = copy.copy(self.queues_list[self.query].get())

            self.state = self.updateState(prevEntities, newEntities) #, action)

            #**********
            self.confidentVote(self.currentEntities, newEntities)
            #self.currentEntities = self.reconcileStates(self.currentEntities, newEntities, action)
            #reward, current_Entities = self.ComputeReward(self.currentEntities, prevEntities)

            #self.currentEntities = copy.copy(current_Entities)
            #**********

        elif action == 'STOP':
            self.terminal = True

        #return self.state, reward, self.terminal


#TEST
e = Environment(1390)
e.step("AcceptU")



#{"RN": {"entity": [], "confidenceScore": []}, "U": {"entity": [], "confidenceScore": []}, "Y": {"entity": [], "confidenceScore": []}}