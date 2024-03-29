import os
import sys
import time

print("make sure all dependencies are at the top! (Like smash::phx::Hash40)")

#uncomment this
import tkinter as tk
from tkinter import filedialog

help_me = """
-ACMD2SMASHSCRIPT-
how to use in command line:
py acmd2smashscript.py [input file] [output file]
or you can drag your mod.rs onto acmd2smashscript
"""

root = tk.Tk()
root.withdraw()
if len(sys.argv) > 1:
  if str(sys.argv[1]) in ["-h", "--help"]:
    print(help_me)
    time.sleep(2.5)
    sys.exit()
  input_file = str(sys.argv[1])
  if len(sys.argv) > 2:
    output_file = str(sys.argv[2])
  else:
    output_file = "mod.rs"
else:
  input_file = filedialog.askopenfilename()
  output_file = "mod.rs"
"""
try:
    args = sys.argv 
    args.pop(0)
    input_file = "".join(args)
    with open(input_file) as f:
      print("")
    f.close()
except Exception:
"""

#comment this
#input_file = "test.rs"

i = []
o = []

sv_animc = []
sv_animcd = []
alphabe = []
alphabet = []
replac = []
replace = []

with open("resource/sv_animcd.txt") as f:
  sv_animc = f.readlines()
f.close()
with open("resource/alphabet.txt") as f:
  alphabe = f.readlines()
f.close()
with open("resource/replace.txt") as f:
  replac = f.readlines()
f.close()

for f in replac:
  f = f.replace("\n", "") 
  f = f.replace("\t", "") 
  f = f.replace(" ", "") 
  replace.append(f)

for f in alphabe:
  f = f.replace("\n", "") 
  f = f.replace("\t", "") 
  f = f.replace(" ", "") 
  alphabet.append(f)

for f in sv_animc:
  f = f.replace("\n", "") 
  f = f.replace("\t", "") 
  sv_animcd.append(f)

def inputter():
  global i
  try:
    with open(input_file) as f:
      i = f.readlines()
    f.close()
  except FileNotFoundError:
    input("File not found!")
    raise

def acmd2smashscript():
  global i
  global o
  is_replacing = False
  acmd_count = 0
  if "use smash::app::sv_animcmd::*;\n" not in i:
    o.append("use smash::app::sv_animcmd::*;\n")
  if "use smash::phx::Hash40;\n" not in i:
    o.append("use smash::phx::Hash40;\n")
  if "use smash_script::*;\n" not in i:
    o.append("use smash_script::*;\n")
  if "use smash::hash40;\n" not in i:
    o.append("use smash::hash40;\n")
  if "use smash::lib::lua_const::*;\n" not in i:
    o.append("use smash::lib::lua_const::*;\n")
  if "use smash::app::lua_bind::*;\n" not in i:
    o.append("use smash::app::lua_bind::*;\n")
  for f in i:
    w_f = f
    if "acmd!(" in f:
      is_replacing = True
      acmd_count += 1
    if "(fighter: &mut L2CFighterCommon) {" in f:
      is_replacing = False
    if "(fighter_base : &mut L2CFighterBase) {" in f:
      is_replacing = False
    if "#[fighter_frame" in f:
      is_replacing = False
    if "#[fighter_frame_callback" in f:
      is_replacing = False
    if "#[status_script" in f:
      is_replacing = False
    if "pub fn install() {" in f:
      is_replacing = False
    if is_replacing == True:
      for x in sv_animcd:
        is_replace = False
        if is_replace == False:
          check_command = w_f.replace("	", "")
          try:
            is_entire_command = check_command[0] == x[0] and check_command[len(x)] == "(" and check_command[len(x)-1] == x[-1]
          except IndexError:
            continue
          if x in w_f and "macros::" not in w_f and is_entire_command:
            w_f = w_f.replace(x+"(", "macros::"+x+"(fighter, ", 1)
            is_replace = True
      w_f = w_f.replace("LUA_VOID", "None")
      w_f = w_f.replace("(is_execute)", "(is_excute)")
      w_f = w_f.replace("rust{", "if true{")
      w_f = w_f.replace("rust {", "if true{")
      if "if(is_excute){" in w_f:
          w_f = w_f.replace("if(is_excute){", "if macros::is_excute(fighter) {")
      if "if(is_excute) {" in w_f:
          w_f = w_f.replace("if(is_excute) {", "if macros::is_excute(fighter) {")
      if "ATTACK(" in w_f and "macros::ATTACK(fighter, " not in w_f:
          w_f = w_f.replace("ATTACK(","macros::ATTACK(fighter, ")
      if "frame(" in w_f and "frame(fighter.lua_state_agent, " not in w_f and "_frame(" not in w_f and "lua_state" not in w_f:
          if "." not in w_f:
            w_f = w_f.replace(")",".0)")
          w_f = w_f.replace("frame(","frame(fighter.lua_state_agent, ")
          w_f = w_f.replace("Frame=","")
      if "wait(" in w_f and "wait(fighter.lua_state_agent, " not in w_f:
          if "." not in w_f:
            w_f = w_f.replace(")",".0)")
          w_f = w_f.replace("wait(","wait(fighter.lua_state_agent, ")
          w_f = w_f.replace("Frames=","")
          w_f = w_f.replace("frames=","")
      if "=" in w_f:
        for i in replace:
          f = i.replace("=", "")
          w_f = w_f.replace("("+i, "(/*"+f+"*/ ")
          w_f = w_f.replace(" "+i, " /*"+f+"*/ ")
          w_f = w_f.replace(","+i, ",/*"+f+"*/ ")
      w_f = w_f.replace("sv_module_access::damage(", "damage!(fighter, ")
      w_f = w_f.replace("sv_module_access::shield(", "shield!(fighter, ")
      w_f = w_f.replace("sv_module_access::grab(", "grab!(fighter, ")
      banlist = ["sv_kinetic_energy", "sv_math", "sv_module_access", "sv_system", "sv_animcmd"]
      is_illegal = False
      for x in banlist:
        if x in w_f:
            is_illegal = True
            break
      if "fighter" not in w_f and "::" in w_f and is_illegal == False and "module_accessor" not in w_f and "boma" not in w_f:
        if "()" not in w_f:
          w_f = w_f.replace("(", "(fighter.module_accessor, ", 1)
        else:
          w_f = w_f.replace("(", "(fighter.module_accessor", 1) 
      if "use" not in w_f:
        w_f = w_f.replace("hash40", "Hash40::new")
      if ";" not in w_f:
        if len(w_f) > 1:
          if w_f[-2] == ")":
            w_f = w_f.replace("\n", ";\n")
      if "for(" in w_f and "Iterations" in w_f:
        iter = w_f.split("for(")
        iterations = iter[1]
        indent = iter[0]
        iterations = iterations.replace("Iterations", "")
        iterations = iterations.replace(")", "")
        iterations = iterations.replace("{", "")
        w_f = indent + "for _ in 0.." + iterations + " {\n"
      for x in alphabet:
        if x in w_f:
            comma = ","+x
            comma2 = ", "+x
            bracket = "("+x
            comment = "*/"+x
            comment2 = "*/ "+x
            if comma in w_f:
              w_f = w_f.replace(comma, ",*"+x)
            if bracket in w_f:
              w_f = w_f.replace(bracket, "(*"+x)
            if comma2 in w_f:
              w_f = w_f.replace(comma2, ", *"+x)
            if comment in w_f:
              w_f = w_f.replace(comment, "*/ *"+x)
            if comment2 in w_f:
              w_f = w_f.replace(comment2, "*/ *"+x)
      w_f = w_f.replace("*Hash40", "Hash40")
      w_f = w_f.replace("*None", "None")
      if "acmd!(lua_state, {"  in w_f:
        w_f = w_f.replace("acmd!(lua_state, {\n", "")
        w_f = w_f.replace("acmd!(lua_state, {", "")
        w_f = w_f.replace(" ", "")
      if "acmd!({"  in w_f:
        w_f = w_f.replace("acmd!({\n", "")
        w_f = w_f.replace("acmd!({", "")
        w_f = w_f.replace(" ", "")
      if "});"  in w_f:
        w_f = w_f.replace("});\n", "")
        w_f = w_f.replace("});", "")
        w_f = w_f.replace(" ", "")
        acmd_count -= 1
        if acmd_count <= 0:
          acmd_count = 0
          is_replacing = False
      if w_f.find("/*X2*/") != -1:
        new = w_f.find("/*X2*/") + 7
        if w_f[new] != "N":
          w_f = w_f.replace("/*X2*/ ", "/*X2*/ Some(")
          w_f = w_f.replace(", /*Y2*/", "), /*Y2*/")
      if w_f.find("/*Y2*/") != -1:
        new = w_f.find("/*Y2*/") + 7
        if w_f[new] != "N":
          w_f = w_f.replace("/*Y2*/ ", "/*Y2*/ Some(")
          w_f = w_f.replace(", /*Z2*/", "), /*Z2*/")
      if w_f.find("/*Z2*/") != -1:
        new = w_f.find("/*Z2*/") + 7
        if w_f[new] != "N":
          w_f = w_f.replace("/*Z2*/ ", "/*Z2*/ Some(")
          w_f = w_f.replace(", /*Hitlag*/", "), /*Hitlag*/")
          w_f = w_f.replace(", /*Status*/", "), /*Status*/")
      if "let lua_state = fighter.lua_state_agent;"  in w_f:
        w_f = w_f.replace("    let lua_state = fighter.lua_state_agent;\n", "          let lua_state = fighter.lua_state_agent;\n")
        w_f = w_f.replace("    let lua_state = fighter.lua_state_agent;", "  let lua_state = fighter.lua_state_agent;")
    o.append(w_f)

inputter()
acmd2smashscript()


if os.path.exists(output_file):
  os.remove(output_file)
with open(output_file, 'a') as f:
  for x in o:
    f.write(x)
f.close()

print("Done!")
