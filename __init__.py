from binaryninja import *
from binaryninja.interaction import get_open_filename_input

highlights_addrs = None

def do_highlighting(bv):
	bv: BinaryView
	file = get_open_filename_input('Load file')
	
	global highlights_addrs
	with open(file, 'rb') as f:
		data = f.read()
		highlights_addrs = data.splitlines()
	
	

	if highlights_addrs is None:
		show_message_box("Parsing Error", "Parsing Error!\n Please check the coverage file format", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)
		return
	
	for instr in highlights_addrs:
		instr_addr = int(instr, 16)
		func = bv.get_functions_containing(instr_addr)
		if len(func) < 1:
			continue
		
		try:
			function = func[0]
			function.set_user_instr_highlight(instr_addr, HighlightStandardColor.BlueHighlightColor)
		except:
			pass

	show_message_box("Complete!", "Complete highlighting!\n\n If that doesn't work, rebase and try again!", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.InformationIcon)

def clear_highlights(bv):
	global highlights_addrs
	
	if highlights_addrs is None:
		return
	
	for instr in highlights_addrs:
		instr_addr = int(instr, 16)
		func = bv.get_functions_containing(instr_addr)
		if len(func) < 1:
			continue
		
		try:
			function = func[0]
			function.set_user_instr_highlight(instr_addr, HighlightStandardColor.NoHighlightColor)
		except:
			pass

	show_message_box("Clear!", "Complete clear highlighting!\n\n If that doesn't work, rebase and try again!", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.InformationIcon)
	

PluginCommand.register("Simple-Coverage\\clear highlights", "clear all highlights", clear_highlights)
PluginCommand.register("Simple-Coverage\\load coverage", "load instructinos from file and highlighting them", do_highlighting)
