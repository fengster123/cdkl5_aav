#%%
MOUSE_COST=800_000
STAGE1_MONKEY_COST=1_000_000
STAGE2_MONKEY_COST=2_000_000
AAV_COST=400_000 # per family
CLINICAL_COST=50_000 # per family
NUMBER_OF_OTHER_FAMILIES=4
I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1=3
IF_RESIDUAL_FAMILY_PAY_10PERCENT_OF_STAGE1_MONKEY_COST=0.1

#%%
# this is for the other families
_each_mouse_cost=MOUSE_COST/(NUMBER_OF_OTHER_FAMILIES + I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1)
_each_stage1_monkey_cost=STAGE1_MONKEY_COST/(NUMBER_OF_OTHER_FAMILIES + I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1)
_each_stage2_monkey_cost=STAGE2_MONKEY_COST*IF_RESIDUAL_FAMILY_PAY_10PERCENT_OF_STAGE1_MONKEY_COST
_each_aav_cost=AAV_COST
_each_clinical_cost=CLINICAL_COST
print(
    f'_each_mouse_cost = {_each_mouse_cost}\n'
    f'_each_stage1_monkey_cost = {_each_stage1_monkey_cost}\n'
    f'_each_stage2_monkey_cost = {_each_stage2_monkey_cost}\n'
    f'_each_aav_cost = {_each_aav_cost}\n'
    f'_each_clinical_cost = {_each_clinical_cost}'
)
_total_each=_each_mouse_cost + _each_stage1_monkey_cost + _each_stage2_monkey_cost + _each_aav_cost + _each_clinical_cost
print(f'_total_each = {_total_each}')
#%%
# this is for me
_my_mouse_cost=MOUSE_COST * I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1/(I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1 + NUMBER_OF_OTHER_FAMILIES)
_my_stage1_monkey_cost=STAGE1_MONKEY_COST * I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1/(I_REPRESENT_NUMBER_OF_FAMILIES_IN_MOUSE_COST_AND_STAGE1 + NUMBER_OF_OTHER_FAMILIES)
_my_stage2_monkey_cost=STAGE2_MONKEY_COST * (1- IF_RESIDUAL_FAMILY_PAY_10PERCENT_OF_STAGE1_MONKEY_COST * NUMBER_OF_OTHER_FAMILIES)
_my_aav_cost=AAV_COST
_my_clinical_cost=CLINICAL_COST
print(
    f'_my_mouse_cost = {_my_mouse_cost}\n'
    f'_my_stage1_monkey_cost = {_my_stage1_monkey_cost}\n'
    f'_my_stage2_monkey_cost = {_my_stage2_monkey_cost}\n'
    f'_my_aav_cost = {_my_aav_cost}\n'
    f'_my_clinical_cost = {_my_clinical_cost}'
)
_total_my=_my_mouse_cost + _my_stage1_monkey_cost + _my_stage2_monkey_cost + _my_aav_cost + _my_clinical_cost
print(f'_total_my = {_total_my}')



#%%
# this is to reconcile
print('supposed total cost is ', _total_each * NUMBER_OF_OTHER_FAMILIES + _total_my)
actual_total_cost=MOUSE_COST+STAGE1_MONKEY_COST+STAGE2_MONKEY_COST+(AAV_COST+CLINICAL_COST)*(NUMBER_OF_OTHER_FAMILIES + 1)
print('actual total cost is ', actual_total_cost)
#%%