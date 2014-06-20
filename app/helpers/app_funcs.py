import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from StringIO import StringIO
'''
THIS FUNCTION SELECTS THE TOP N DRUGS ASSOCIATED WITH AN INDICATION
'''
def first_n_drugs_assoc_indic(n, indication, conn):
	query_string = '''
		SELECT drg.medicinalproduct
		FROM drugs drg
		JOIN indications ind
		ON drg.drug_id = ind.drug_id
		WHERE ind.drugindication = '{0}'
		GROUP BY drg.medicinalproduct
		ORDER BY COUNT(drg.medicinalproduct) DESC
		LIMIT {1}'''.format(indication, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	result = tuple(result_df['medicinalproduct'])
	return result


'''
THIS FUNCTION SELECTS THE TOP N EFFECTS ASSOCIATED WITH AN INDICATION.
TOP N ARE SELECTED BY FIRST SORTING BY THE NUMBER OF SIDE EFFECTS ASSOCIATED
WITH THE DRUG, THEN BY THE SUM OF PROBABILITIES ACROSS DRUGS. 
'''
def first_n_effects(n, indication, conn):
	query_string = '''
		SELECT side_effect, COUNT(side_effect) AS tot_effect_count, SUM(effect_proportion)
		FROM {0}_effect_props
		WHERE side_effect NOT IN ("DRUG INEFFECTIVE", "COMPLETED SUICIDE", "DRUG INTERACTION", "DEPRESSION")
		GROUP BY side_effect
		ORDER BY tot_effect_count DESC, SUM(effect_proportion) DESC
		LIMIT {1}'''.format(indication, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	result = list(result_df['side_effect'])
	return result


def get_side_effect_probabilities(side_effect_tuple, indication, conn):
	query_string = '''
		SELECT side_effect, medicinalproduct, effect_proportion
		FROM {0}_effect_props
		WHERE side_effect IN {1}'''.format(indication, side_effect_tuple)
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df
	

# def plot_single_effect(pd_slice):
# 	'''Expects pandas data slice of side effects and drug name'''
# 	side_effects=list(pd_slice.index)
# 	probs=list(pd_slice)
# 	#plt.figure(); # attempt 1
# 	#pd_slice.plot(kind='bar') # attempt 1
# 	#plt.axhline(0, color='k') # attempt 1
# 	fig.add_subplot(1,1,1) # attempt 2
# 	plt.plot(probs) # attempt 2
# 	plt.xlabel('side effect')
# 	plt.ylabel('proportion of reported cases')
# 	plt.xticks(rotation=45)
# 	plt.title(pd_slice.name, color='black')
# 	#plt.autofmt_xdate()
# 	html = mpld3.fig_to_html(fig)
# 	return html

def plot_single_effect(pd_slice):
	'''Expects pandas data slice of side effects and drug name'''
	fig=plt.figure();
	pd_slice.plot(kind='bar')
	plt.axhline(0, color='k')
	plt.xlabel('side effect')
	plt.ylabel('proportion of reported cases')
	plt.xticks(rotation=45)
	plt.title(pd_slice.name, color='black')
	fig.autofmt_xdate(rotation=45, ha='right')
	img = StringIO()
	fig.savefig(img)
	img.seek(0)
	return img

