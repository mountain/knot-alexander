# --- SageMath Code - Approach 5: Simplify then Isomorphism (Corrected AssignName) ---
import tempfile
import os

print("--- Running GAP Script via File (with Simplification) ---")

# Ensure F_R, G_R, F_HNN, G_HNN are defined in Sage first
F_R.<aR, bR> = FreeGroup('aR, bR')
# Assuming R = abbbaBAAB is correct as it's from snappy
relator_R = aR * bR ** 3 * aR * bR ** -1 * aR ** -2 * bR ** -1
G_R = F_R / [relator_R]

F_HNN.<uH, vH, tH> = FreeGroup('uH, vH, tH')
relator_HNN1 = tH ** -1 * uH * tH * vH ** -1 * uH ** -1
relator_HNN2 = tH ** -1 * vH * tH * vH ** -1 * uH ** -1 * vH ** -1
G_HNN = F_HNN / [relator_HNN1, relator_HNN2]

print("Preparing full GAP script with simplification...")

gen_R_names_str = '"aR_g", "bR_g"'
gen_HNN_names_str = '"uH_g", "vH_g", "tH_g"'
rel_R_str_gap = "aR_g_free * bR_g_free^3 * aR_g_free * bR_g_free^-1 * aR_g_free^-2 * bR_g_free^-1"
rel_HNN1_str_gap = "tH_g_free^-1 * uH_g_free * tH_g_free * vH_g_free^-1 * uH_g_free^-1"
rel_HNN2_str_gap = "tH_g_free^-1 * vH_g_free * tH_g_free * vH_g_free^-1 * uH_g_free^-1 * vH_g_free^-1"

# Construct the entire GAP script *without* AssignName for groups
gap_script = f"""
# --- GAP Script Start ---
Print("--- Starting GAP Script ---\\n");;

# Define G_R original
Print("Defining GR_g_orig...\\n");;
FreeR_g := FreeGroup({gen_R_names_str});;
aR_g_free := GeneratorsOfGroup(FreeR_g)[1];;
bR_g_free := GeneratorsOfGroup(FreeR_g)[2];;
RelR_gap_word := {rel_R_str_gap};; 
GR_g_orig := FreeR_g / [RelR_gap_word];; 
Print("GR_g_orig defined.\\n");;

# Define G_HNN original
Print("Defining GHNN_g_orig...\\n");;
FreeHNN_g := FreeGroup({gen_HNN_names_str});;
uH_g_free := GeneratorsOfGroup(FreeHNN_g)[1];;
vH_g_free := GeneratorsOfGroup(FreeHNN_g)[2];;
tH_g_free := GeneratorsOfGroup(FreeHNN_g)[3];;
RelHNN1_gap_word := {rel_HNN1_str_gap};;
RelHNN2_gap_word := {rel_HNN2_str_gap};;
GHNN_g_orig := FreeHNN_g / [RelHNN1_gap_word, RelHNN2_gap_word];;
Print("GHNN_g_orig defined.\\n");;

# Simplify the presentations
Print("Simplifying presentations...\\n");;
GR_g := SimplifiedFpGroup(GR_g_orig);;
Print("GR_g simplified.\\n");;
# Print(GR_g); 

GHNN_g := SimplifiedFpGroup(GHNN_g_orig);;
Print("GHNN_g simplified.\\n");;
# Print(GHNN_g); 

# Attempt isomorphism on *simplified* groups
Print("Attempting isomorphism GHNN_g_simplified -> GR_g_simplified...\\n");;
iso_simplified := IsomorphismFpGroup(GHNN_g, GR_g);; 

if iso_simplified = fail then
    Print("Isomorphism not found between *simplified* groups. Checking again...\\n");;
    are_iso := AreIsomorphicFpGroup(GHNN_g, GR_g);; # On simplified
    Print("AreIsomorphicFpGroup on simplified returns: ", are_iso, "\\n");;
    Print("Checking isomorphism on original groups again...\\n");;
    are_iso_orig := AreIsomorphicFpGroup(GHNN_g_orig, GR_g_orig);;
    Print("AreIsomorphicFpGroup on original returns: ", are_iso_orig, "\\n");;
    if are_iso_orig = false then 
         Print("\\n*** Error: Original groups determined non-isomorphic by GAP. Check presentations. ***\\n");;
    fi;
else
    Print("Isomorphism found between *simplified* groups!\\n");;
    Print("Attempting to get isomorphism between *original* groups again...\\n");;
    iso_orig := IsomorphismFpGroup(GHNN_g_orig, GR_g_orig);;

    if iso_orig = fail then
         Print("Could not get isomorphism mapping between original groups directly.\\n");;
         Print("Try composing simplification maps manually if mapping is needed.\\n");;
    else
         Print("Isomorphism mapping between original groups found!\\n");;
         iso := iso_orig;; 
         inv_iso := InverseMapping(iso);;

         gens_GHNN_g := GeneratorsOfGroup(GHNN_g_orig);; 
         gens_GR_g := GeneratorsOfGroup(GR_g_orig);; 

         uH_g_fp := fail; vH_g_fp := fail; tH_g_fp := fail;
         if Length(gens_GHNN_g) >= 3 then
             uH_g_fp := gens_GHNN_g[1];; vH_g_fp := gens_GHNN_g[2];; tH_g_fp := gens_GHNN_g[3];;
         else Print("\\n*** Warning: GHNN_g_orig has < 3 generators? Mapping might be incomplete. ***\\n");;

         aR_g_fp := fail; bR_g_fp := fail;
         if Length(gens_GR_g) >= 2 then
             aR_g_fp := gens_GR_g[1];; bR_g_fp := gens_GR_g[2];;
         else Print("\\n*** Warning: GR_g_orig has < 2 generators? Mapping might be incomplete. *** \\n");;

         if uH_g_fp <> fail and aR_g_fp <> fail then 
             Print("Mapping HNN -> R (Original Generators):\\n");;
             Print("uH maps to: ", Image(iso, uH_g_fp), "\\n");;
             Print("vH maps to: ", Image(iso, vH_g_fp), "\\n");;
             if tH_g_fp <> fail then 
                  Print("tH maps to: ", Image(iso, tH_g_fp), "\\n");;
             fi;;

             Print("Mapping R -> HNN (Original Generators):\\n");;
             Print("aR maps to: ", Image(inv_iso, aR_g_fp), "\\n");;
             Print("bR maps to: ", Image(inv_iso, bR_g_fp), "\\n");;
         fi;;
    fi;
fi;;

Print("--- GAP Script Finished ---\\n");;
# --- GAP Script End ---
"""

# Execute the whole script using gap.eval() via file
tmp_filename = ""
try:
    # ... (rest of the file writing and execution code remains the same) ...
    with tempfile.NamedTemporaryFile(mode='w', suffix='.g', delete=False, encoding='utf-8') as tmp_file:
        tmp_filename = tmp_file.name
        tmp_file.write(gap_script)
    print(f"GAP script written to temporary file: {tmp_filename}")
    gap_read_cmd = f'Read("{tmp_filename}");'
    print(f"Executing GAP command: {gap_read_cmd}")
    gap_output = gap.eval(gap_read_cmd)
    print("\n--- GAP Output ---")
    print(gap_output)
    print("--- End GAP Output ---")
except Exception as e:
    print(f"\nAn error occurred during execution via file: {e}")
    import traceback

    traceback.print_exc()
finally:
    if tmp_filename and os.path.exists(tmp_filename):
        try:
            os.remove(tmp_filename)
        except OSError as e:
            print(f"Error removing temp file: {e}")
        else:
            print(f"Temporary file {tmp_filename} removed.")

print("-" * 20)
print("Note: Assumes the presentation R = abbbaBAAB = 1 from snappy is correct for the 4_1 knot.py group.")