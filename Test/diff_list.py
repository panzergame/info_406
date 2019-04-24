def diff_list(a, b):
	set_a = set(a)
	set_b = set(b)

	added_keys = set_a - set_b
	removed_keys = set_b - set_a
	kept_keys = set_a & set_b

	return added_keys, removed_keys, kept_keys

def diff_dict(a, b):
	set_a = set(a.keys())
	set_b = set(b.keys())

	added_keys = set_a - set_b
	removed_keys = set_b - set_a
	kept_keys = set_a & set_b

	added_dict = {key : a[key] for key in added_keys}
	removed_dict = {key : b[key] for key in removed_keys}
	kept_dict = {key : a[key] for key in kept_keys}

	for key in kept_keys:
		if isinstance(a[key], list):
			added, removed, kept = diff_list(a[key], b[key])
			added_dict[key] = added
			removed_dict[key] = removed
			kept_dict[key] = kept

	return added_dict, removed_dict, kept_dict

diff_dict({"a" : 8, "c" : 7, "e" : [2, 8]}, {"b" : 8, "c" : 7, "e" : [8, 5], "t" : []})
	
