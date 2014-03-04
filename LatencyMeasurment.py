

"""because I want to encapsulate all the latency measurement stuff
   I have to do use a dedicated class for it
   cant just have one method, because I need to handle the stats recieved event
   measure latency for one single switch """
import time
import openflow.libopenflow_01 as of
from pox.core import core

"""call this in the run method. forget about latency tpye, just return raw results"""
   
class LatencyMeasurment():
    
    def __init__(self,switchOne,switchTwo):
        
        s1 = None
        s2 = None
        for switchDPID in self.switches:
            if switchOne.strip() == pox.lib.util.dpid_to_str(switchDPID):
                s1 = self.switches[switchDPID]
            if switchTwo.strip() == pox.lib.util.dpid_to_str(switchDPID):
                s2 = self.switches[switchDPID]
        outPort = self.getOutPort(s1, s2)      
       
        
        core.openflow.addListenerByName("PacketIn",self.handlePacketIn)
        core.openflow.addListenerByName("FlowStatsReceived",self.handleStatsReply)
        self.latency = 0
        
    
        self.switchOneRTT = self.measureLatency(s1)
        self.switchTwoRTT = self.measureLatency(s2)
        
        self.sendLatencyFlowMod(switchOne)
        time.sleep(1)
        self.sendLatencyEthernetPacket(outPort, switchOne)
        
        
        
        
    def sendStatsRequest(self,switch):
        startTime = time.time() 
        switch.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
        return startTime
        
    
    def measureLatency(self,switch):
        self.endTime = 0
        startTime = sendStatsRequest(switch)
        """wait for the reply"""
        while (self.endTime == 0): 
            pass
        return self.endTime - startTime
        
        
        
        
        
    def handleStatsReply(self,event):
        #should be the only stats reply, but check anyway
        if event.connection == self.switch:
            self.endTime = time.time()
            
            
    def sendLatencyFlowMod(self,switch):
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0001
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
        switch.send(msg)
        
    """maybe put specific links as well, in the packet, so can measure a lot at once"""
    def sendLatencyEthernetPacket(self,outPort,switch):
        ether = pkt.ethernet()
        #effective_ethertype
        ether.type = 0001 #arbitary type, taken from paper
        ether.dst = EthAddr("ff:ff:ff:ff:ff:ff")
        ether.src = EthAddr("01:02:03:04:05:06")
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=outPort)
        msg.actions.append(action)
        self.timeStamp= time.time()
    
        msg.data = ether
        print "sending ethernet packet"
        switch.send(msg)
        
    def handlePacketIn(self,event):
        packet = event.parsed
        ether = packet.find('ethernet')
        if ether and ether.type==0001: 
            finish = time.time()
            tTotal = finish - self.timeStamp 
            self.latency = tTotal -((self.switchOneRTT/2) + (self.switchTwoRTT/2))
            
            
            
    """put in switch objects, get outport back"""
    def getOutPort(self,s1,s2):
        coreOne = ("00-00-00-04-01-01",{"00-00-00-00-02-01":1,"00-00-00-01-02-01":2,"00-00-00-02-02-01":3,"00-00-00-03-02-1":4})
        coreTwo = ("00-00-00-04-01-02",{"00-00-00-00-02-01":1,"00-00-00-01-02-01":2,"00-00-00-02-02-01":3,"00-00-00-03-02-1":4})
        coreThree = ("00-00-00-04-02-01",{"00-00-00-00-03-01":1,"00-00-00-01-03-01":2,"00-00-00-02-03-01":3,"00-00-00-03-03-1":4})
        coreFour = ("00-00-00-04-02-02",{"00-00-00-00-03-01":1,"00-00-00-01-03-01":2,"00-00-00-02-03-01":3,"00-00-00-03-03-1":4})
        
        aggregateOne = ("00-00-00-00-02-01",{"00-00-00-04-01-01":1,"00-00-00-00-00-01":2,"00-00-00-04-01-02":3,"00-00-00-00-01-01":4})
        aggregateTwo = ("00-00-00-00-03-01",{"00-00-00-04-02-01":1,"00-00-00-00-00-01":2,"00-00-00-04-02-02":3,"00-00-00-00-01-01":4})
        aggregateThree = ("00-00-00-01-02-01",{"00-00-00-04-01-01":1,"00-00-00-01-00-01":2,"00-00-00-04-01-02":3,"00-00-00-01-01-01":4})
        aggregateFour = ("00-00-00-01-03-01",{"00-00-00-04-02-01":1,"00-00-00-01-00-01":2,"00-00-00-04-02-02":3,"00-00-00-01-01-01":4})
        aggregateFive = ("00-00-00-02-02-01",{"00-00-00-04-01-01":1,"00-00-00-02-00-01":2,"00-00-00-04-01-02":3,"00-00-00-02-01-01":4})
        aggregateSix = ("00-00-00-02-03-01",{"00-00-00-04-02-01":1,"00-00-00-02-00-01":2,"00-00-00-04-02-02":3,"00-00-00-02-01-01":4})
        aggregateSeven = ("00-00-00-03-02-01",{"00-00-00-04-01-01":1,"00-00-00-03-00-01":2,"00-00-00-04-01-02":3,"00-00-00-03-01-01":4})
        aggregateEight = ("00-00-00-03-03-01",{"00-00-00-04-02-01":1,"00-00-00-03-00-01":2,"00-00-00-04-02-02":3,"00-00-00-03-01-01":4})
   
        switchMap = [coreOne,coreTwo,coreThree,coreFour,aggregateOne,aggregateTwo,aggregateThree,aggregateFour,aggregateFive,aggregateSix,aggregateSeven,aggregateEight]        
            
        """s1 and s2 is a switch object"""
        s1MAC = (str(s1)[1:-3]).strip()
        s2MAC = (str(s2)[1:-3]).strip()
        outPort = None
       # print  s1MAC +" wants to find the port number for "+s2MAC
        for s in self.switchMap:
            if (s[0]).strip() == s1MAC:
                return s[1][s2MAC]
        return None
            
            
            
            
            
            
            
            
            
            