from alex import check_items_nbttag, check_parents, check_pet_nums, check_sacks, cleanup_snbt, check_snbt, check_misc


def Main():
    check_items_nbttag.Main()
    check_misc.Main()
    check_parents.Main()
    check_pet_nums.check_pets()
    check_sacks.check_all_sacks()
    check_snbt.Main()
    cleanup_snbt.Main()

if __name__ == "__main__":
    Main()
