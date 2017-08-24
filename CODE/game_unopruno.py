"""query types are categorized as ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
as a list of keywords for querying 4 different research engines. """

import  CODE.filter_queues as filter_queues

QUERY_TYPES = ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]
ENTITIES = 3
STATE_SIZE = 3* ENTITIES
ACTIONS = ["query", "AcceptRN", "AcceptU", "AcceptY", "AcceptALL", "STOP"]

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


        self.query = 0 #query type
        self.currentEntities = self.queues_list[self.query].get()


        self.state = [0 for i in range(STATE_SIZE)]
        self.terminal = False

    # updatining the state it should be based on the decision from DQN
    # but we make it randomly at this phase TODO updatign states should be modified based on the DQN agent decision
    def updateState(self, action):
        pass

    def reconcileStates(self, currentEntities, newEntities, action):
        print('currentEntities', currentEntities)
        print('newEntities', newEntities)

        mergeEntities = currentEntities
        if action == ACTIONS[1]:
            mergeEntities["RN"] = newEntities["RN"]
            return mergeEntities

        elif action == ACTIONS[2]:
            mergeEntities["U"] = newEntities["U"]
            return mergeEntities

        elif action == ACTIONS[3]:
            mergeEntities["Y"] = newEntities["Y"]
            return mergeEntities
        else:
            mergeEntities = newEntities
            return mergeEntities


    def ComputeReward(self, currentEntities, prevEntities):
        pass

    def step(self, action):
        if action == "query":
            self.query = (self.query + 1) % len(QUERY_TYPES)

        elif action != "STOP":
            prevEntities = self.currentEntities
            newEntities = self.queues_list[self.query].get()

            self.currentEntities = self.reconcileStates(self.currentEntities, newEntities, action)

            #self.state = self.updateState(action)
            #reward = self.ComputeReward(self.currentEntities, prevEntities)

        #return self.state, reward, self.terminal

#TEST
e = Environment(1390)
e.step("reconcile")



