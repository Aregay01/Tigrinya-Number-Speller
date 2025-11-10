# Number speller implemented as a class, preserving original logic and making the code robust
class NumberSpeller:
    # decimal mappings for single digits including 10 as name for convenience
    decimal_digit = {
        0: "ዜሮ", 1: "ሓደ", 2: "ክልተ", 3: "ሰለስተ", 4: "ኣርባዕተ",
        5: "ሓሙሽስተ", 6: "ሽድስተ", 7: "ሸዋዕተ", 8: "ሾሞንተ", 9: "ትሽዓተ",
        10: "ዓሰርተ",
    }  # maps single digits to their spellings
    # a larger base mapping used by the main spelling routine
    base_number = {
        0: "ዜሮ", 1: "ሓደ", 2: "ክልተ", 3: "ሰለስተ", 4: "ኣርባዕተ",
        5: "ሓሙሽስተ", 6: "ሽድስተ", 7: "ሸዋዕተ", 8: "ሾሞንተ", 9: "ትሽዓተ",
        10: "ዓሰርተ", 20: "ዒስራ", 30: "ሰላሳ", 40: "ኣርብዓ",
        50: "ሓምሳ", 60: "ስሳ", 70: "ሰብዓ", 80: "ሰማንያ", 90: "ቴስዓ",
        100: "ሚእቲ", 1000: "ሽሕ", 10**6: "ሚሊዮን", 10**9: "ቢሊዮን",
    }  # maps bases (tens, hundreds, thousands...) to spellings
    # second-base mapping (tens) copied from base_number for convenience
    Base_2 = {
        10: "ዓሰርተ", 20: "ዒስራ", 30: "ሰላሳ", 40: "ኣርብዓ",
        50: "ሓምሳ", 60: "ስሳ", 70: "ሰብዓ", 80: "ሰማንያ", 90: "ቴስዓ",
    }  # maps the tens to spellings
    # append the 'ን' suffix to the Base_2 mappings and store as a separate dict
    Base_2_with_ን = {k: v + "ን" for k, v in Base_2.items()}  # tens with suffix

    def __init__(self):
        # constructor does nothing special but is present for extensibility
        self.decimal_digit = NumberSpeller.decimal_digit  # instance reference to decimal_digit
        self.base_number = NumberSpeller.base_number  # instance reference to base_number
        self.Base_2 = NumberSpeller.Base_2  # instance reference to Base_2
        self.Base_2_with_ን = NumberSpeller.Base_2_with_ን  # instance reference to Base_2_with_ን

    def digit_count(self, n) -> int:
        # returns the number of digits in the input; accepts int or string
        if isinstance(n, str):
            n = n.strip()  # strip whitespace from the string
            if n.startswith('-'):
                n = n[1:]  # remove leading minus sign if present
            return len(n)  # return the length of the cleaned string
        return len(str(abs(n)))  # for non-strings return length of absolute value string

    def int_sanitiser(self, spelling_list):
        # Removes the word "ሓደ" when it is immediately followed by a Base_2 or Base_2_with_ን word
        i = 0  # start index for iteration
        while i < len(spelling_list) - 1:  # iterate until the second-last index
            curr = spelling_list[i]  # current item at index i
            nxt = spelling_list[i + 1]  # next item at index i+1
            if curr == "ሓደ" and (nxt in self.Base_2_with_ን.values() or nxt in self.Base_2.values()):
                del spelling_list[i]  # delete current item when condition matches
            else:
                i += 1  # otherwise move to next index
        return spelling_list  # return the possibly-modified list

    def int_speller(self, n: int, spelling_list, index):
        # Main recursive spelling routine for integer parts; keeps original logic
        csb = 1  # current significant base initialized to 1 as in original logic
        for key in self.base_number:  # iterate over base_number keys in insertion order
            if n < key:  # when n is less than current key, compute quotient/remainder using csb
                quatient = n // csb  # integer division to get how many csb units in n
                spelling = self.base_number[csb]  # get the spelling for the csb base
                remainder = n % csb  # compute the remainder after removing csb multiples

                if remainder != 0:
                    spelling += "ን"  # append the "ን" suffix when remainder exists

                if remainder in self.base_number:
                    remainder = self.base_number[remainder] + "ን"  # map remainder to word + suffix when possible

                spelling_list[index:index + 1] = [quatient, spelling, remainder]  # replace slice with new items

                index = 0  # reset index to walk and convert integer items to words
                for item in spelling_list:  # iterate through spelling_list
                    if isinstance(item, int):  # only handle integer items
                        if item in self.base_number:
                            spelling_list[index] = self.base_number[item]  # replace known base ints with words
                        else:
                            self.int_speller(item, spelling_list, index)  # recursively spell non-base integer items
                    index += 1  # increment index after handling item

                sanitized = self.int_sanitiser(spelling_list)  # sanitise list according to int_sanitiser rules
                return sanitized  # return sanitized list once processed
            csb = key  # update csb to current key for next iteration

    def spell(self, n):
        # Public API: spell the given number n and return its spelling as a string
        # handle types and create working copies to avoid mutating caller's data
        try:
            n_val = float(n)  # attempt to coerce input to float
        except Exception:
            raise ValueError("Input must be a number or numeric string")  # raise clear error on invalid input

        n_sign = -1 if n_val < 0 else 1  # determine sign of the number
        number = abs(n_val)  # work with absolute value for spelling
        spelling_list = [0]  # initialize spelling list as the original code did
        if int(n_val) == 0:
            int_part_spelling = [self.decimal_digit[0]]  # if integer part is zero, use decimal_digit[0]
            sign = []  # empty sign list when zero
        else:
            int_part_spelling = self.int_speller(int(number), spelling_list, 0)  # call int_speller for integer part
        if n_val < 0:
            sign = ["ኣሉታ"]  # negative sign word when original number negative
        else:
            sign = ""  # empty string when non-negative
        if isinstance(number, float):
            fractional = str(number).split('.')[1]  # get fractional part as string after decimal point
            point = ["ነጥቢ"]  # decimal point word
            fractional_digit_count = self.digit_count(fractional)  # number of digits in fractional part
            fraction_spelling = []  # list to collect fractional digit spellings
            fractional = int(fractional)  # convert fractional string to integer for digit extraction
            for i in range(fractional_digit_count):
                fraction_spelling.append(self.decimal_digit[fractional // (10 ** (fractional_digit_count - 1 - i))])  # append the digit word
                fractional = fractional % (10 ** (fractional_digit_count - i - 1))  # reduce fractional for next digit
        else:
            point = []  # no decimal point for non-floats
            fraction_spelling = []  # empty fractional list for non-floats

        # combine sign, integer part spelling, decimal point, and fractional spellings into one flat list
        spell_list = []  # start with empty list
        if isinstance(sign, list):
            spell_list.extend(sign)  # extend with sign list when sign is list
        elif isinstance(sign, str) and sign:
            spell_list.append(sign)  # append sign string when non-empty
        if isinstance(int_part_spelling, list):
            spell_list.extend(int_part_spelling)  # extend with integer part spelling list
        else:
            spell_list.append(int_part_spelling)  # append integer part spelling when it is a single item
        spell_list.extend(point)  # extend with point list (possibly empty)
        spell_list.extend(fraction_spelling)  # extend with fractional digit spellings

        # coerce all items to strings and join with spaces to form final spelling
        spell_list = [str(x) for x in spell_list]  # ensure all items are strings
        spelling = " ".join(spell_list)  # join items with a space
        return spelling  # return the final spelling string


# Example usage: create an instance and spell the example number (mirrors original main)
if __name__ == "__main__":
    sp = NumberSpeller()  # instantiate the speller class
    result = sp.spell(-230.41)  # spell the example number -230.41
    print("spelling:", result)  # print the resulting spelling string
