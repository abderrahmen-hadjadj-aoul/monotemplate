Some text
!My name is <REPLACE:name>, How are you <REPLACE:name2> ?
!My name is Pierre Dolor, How are you Benoit ? # <REPLACED> 

Bla bla bla

!<REPLACE:node_name> <REPLACE:nodes> <REPLACE:node_x> ! <CHECK> something
!NODE_NAME 4 1 ! <CHECK> something # <REPLACED> 
!NODE_NAME 7 2 ! <CHECK> something # <REPLACED> 
!NODE_NAME 11 3 ! <CHECK> something # <REPLACED> 
!NODE_NAME 55 70000 ! <CHECK> something # <REPLACED> 

!<REPLACE:door> <REPLACE:color>
# <ERROR> Key 'color' not exiting. 

!SYSTEM = <REPLACE:system>
# <ERROR> Key 'system' not exiting. 

...
