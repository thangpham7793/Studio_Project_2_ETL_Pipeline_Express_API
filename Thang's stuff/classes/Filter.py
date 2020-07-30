# This should be run after the columns have been cut and processed
# All conditions will be applied (A & B & C & D ...). A bit simplistic though


class Filter:
    def create_filter(self, df, target_col, target_values_list):
        return df[target_col].apply(lambda x: x in target_values_list)

    def prompt_user_to_filter(self, df):
        # maybe only filter on some obvious columns (status + materials)
        # in that case it's simpler
        for col in df.columns:
            # skip columns that have too many unique values
            unique_value_counts = len(df[col].unique())
            if unique_value_counts >= 20 or unique_value_counts == 1:
                continue
            user_input = input(
                f"Column {col.upper()} has {unique_value_counts} values.\nWould you like to decide which values to keep? Y/N\n"
            )
            invalid_input = True
            while invalid_input:
                if user_input.isalpha() == False:
                    user_input = input("Please enter Y or N\n")
                elif user_input.lower() not in ["y", "ye", "yes", "n", "no"]:
                    user_input = input("Please enter Y or N\n")
                else:
                    invalid_input = False
            print(f"Proceed!")
