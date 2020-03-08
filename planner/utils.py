class ShoppingList:
    amount_list = []
    unit_list = []
    name_list = []
    
    def append_ingredient(self, ingred):
        if ingred.name not in self.name_list:
            self.amount_list.append(ingred.amount)
            self.unit_list.append(ingred.unit)
            self.name_list.append(ingred.name)
        else:
            existing_item_index = self.name_list.index(ingred.name)
            existing_item_unit = self.unit_list[existing_item_index]

            if ingred.unit == existing_item_unit:
                if self.amount_list[existing_item_index] is None:
                    self.amount_list[existing_item_index] = ingred.amount
                else:
                    if ingred.amount is None:
                        ingred.amount = 0.0
                
                    self.amount_list[existing_item_index] += ingred.amount
            else:
                self.amount_list.append(ingred.amount)
                self.unit_list.append(ingred.unit)
                self.name_list.append(ingred.name)


    def retrieve(self):
        shopping_list = []

        for i in range(len(self.amount_list)):
            if self.amount_list[i] is None:
                shopping_list.append('{} {}'.format(self.unit_list[i], self.name_list[i]))
            else:
                shopping_list.append('{:.1f} {} {}'.format(self.amount_list[i], self.unit_list[i], self.name_list[i]))

        return shopping_list
 