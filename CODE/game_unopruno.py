"""query types are categorized as ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
as a list of keywords for querying 4 different research engines. """
import copy
import numpy as np

import CODE.filter_queues as filter_queues

QUERY_TYPES = ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
ENTITIES_NUM = 3
ENTITIES_LIST = ["RN", "U", "Y"]
STATE_SIZE = 4* ENTITIES_NUM
ACTIONS = ["AcceptRN", "AcceptU", "AcceptY", "AcceptALL", "STOP"]
EMPTY_ENTITIES_CONFIDENCE_SCORE = {'RN': {'entity': [], 'confidenceScore': []}, 'U': {'entity': [], 'confidenceScore': []}, 'Y': {'entity': [], 'confidenceScore': []}}

#Environment for each episode (person_id)
class Environment:
    def __init__(self, person_id, args):
        self.person_id = str(person_id)
        self.path = "../DATA/entities_db/"+ self.person_id + '/queue_'

        #save extracted entities from queries in queues
        t = filter_queues.queires_to_queue(self.person_id)

        #list of queues inclusing the entities indexes in ../DATA/entities_db/person_id folder
        #indexes of queues_list come from  QUERY_TYPES = ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
        self.queues_list = t.filter_queues_save_indexes()
        self.originalEntities = t.originalEntities
        #self.BestEntities_Bestscores = {'RN': {'entity': [], 'confidenceScore': []}, 'U': {'entity': [['Epic', 'Willow']], 'confidenceScore': [0.5]}, 'Y': {'entity': [], 'confidenceScore': []}}

        self.query_type = 0 #query type
        self.currentEntities = self.queues_list[self.query_type].get()
        self.BestEntities_BestConfidence = self.currentEntities

        self.state = [0.0 for i in range(STATE_SIZE)]
        self.terminal = False

        """arguments for the class"""
        self.aggregate = args.aggregate #it signifies the value reconcilation method: Confidence, Majority
        self.queryTypes = QUERY_TYPES

        #this variable is to get list of all extracted universities and years
        self.University_Year_list = np.array(['U','Y'])

    #several various methods for selecting the best entities after each reconcilation
    #*********************************
    def majorityVote(self):
        pass

    #TODO this method is based on tchoosing the entity values with the hoghest confident score. but since most the confident score are
    #0.5, it does not work properly.
    def confidentVote(self, currEntities, NewEntities):
        print ('currEntities', currEntities)
        print('NewEntities',NewEntities)

        print('BestEntities_BestConfidence', self.BestEntities_BestConfidence)

        self.BestEntities_BestConfidence = EMPTY_ENTITIES_CONFIDENCE_SCORE

        for ent in ENTITIES_LIST:
            entities = []
            scores = []

            [entities.append(elem) for elem in currEntities[ent]['entity']]
            [entities.append(elem) for elem in NewEntities[ent]['entity']]

            [scores.append(elem) for elem in currEntities[ent]['confidenceScore']]
            [scores.append(elem) for elem in NewEntities[ent]['confidenceScore']]

            if scores:
                index = scores.index(max(scores))
                self.BestEntities_BestConfidence[ent]['entity'] = entities[index]
                self.BestEntities_BestConfidence[ent]['confidenceScore'] = scores[index]

        self.currentEntities = copy.copy(self.BestEntities_BestConfidence)
        self.University_Year_list = np.append( self.University_Year_list, [ [self.BestEntities_BestConfidence['U']['entity']],
                                                                               [self.BestEntities_BestConfidence['Y']['entity']] ], axis=0)
        return
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
    # but we make it randomly at this phase TODO updating states should be modified based on the DQN agent decision
    def updateState(self, currEntities, newEntities):

        """the part for computing states in each iteration"""
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

        """self.currentEntities should be modified for continuing the process"""
        if self.aggregate == 'cofidence':
            self.confidentVote(currEntities, newEntities)

        return

    #TODO
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
                #currentEntities[entity] = check_result_current[1]
            if(check_result_prev[0]):
                sum_reward -= reward_unit

        return sum_reward #, currentEntities

    #TODO in the origninal paper, the agent select two options query or reconcilation every time but here I separated queries
    # like another action until now.
    # take a single step in the episode
    def step(self, action, query_type):
        """

        :param action:
        :param query_type: is the selected query type by the agent
        :return:
        """
        reward = 0.0


        self.query_type = (query_type) % len(self.queryTypes)

        if action != "STOP":

            #if the queue is not empty
            if not self.queues_list[self.query_type].Empty:
                newEntities = copy.copy(self.queues_list[self.query_type].get())
                prevEntities = copy.copy(self.currentEntities)

                self.state = self.updateState(prevEntities, newEntities) #, action)

                #**********
                #TODO I do not undertand the difference between reconcileStates w.r.t action and various aggretion (baseline) methods
                self.confidentVote(self.currentEntities, newEntities)
                #self.currentEntities = self.reconcileStates(self.currentEntities, newEntities, action)
                reward = self.ComputeReward(self.currentEntities, prevEntities)

                #**********
            else:
                self.queryTypes = self.queryTypes[:query_type] + self.queryTypes[query_type+1 :]


        elif action == 'STOP':
            self.terminal = True

        return self.state, reward, self.terminal


#TEST
e = Environment(1390)
e.step("AcceptU")



