class Item():
    def __init__(self, barcode, name, price, item_type):
        self.item_barcode = str(barcode)
        self.item_name = name
        self.item_price = price
        self.item_type = item_type

    def getBarcode(self):
        return self.item_barcode

    def getName(self):
        return self.item_name

    def getPrice(self):
        return self.item_price

    def getType(self):
        return self.item_type


class Cart():
    def __init__(self):
        self.cart_item = {}

    def addItem(self, barcode, name, price, item_type, quality = None):
        item = Item(barcode, name, price, item_type)
        is_exist = self.isExist(barcode)

        if is_exist:
            self.cart_item[is_exist] += 1
        else:
            if quality:
                self.cart_item[item] = quality
            else:
                self.cart_item[item] = 1
    
    def getItem(self):
        print(self.cart_item)
        return self.cart_item

    def getBarcode(self):
        barcode_list = []
        for item in self.cart_item:
            barcode_list.append(item.getBarcode())
        print(barcode_list)
        return barcode_list

    def getName(self):
        name_list = []
        for item in self.cart_item:
            name_list.append(item.getName())
        print(name_list)
        return name_list

    def getPrice(self):
        price_list = []
        for item in self.cart_item:
            price_list.append(item.getPrice())
        print(price_list)
        return(price_list)

    def getCartPrice(self):
        total = 0
        for item in self.cart_item:
            total += item.getPrice() * int(self.cart_item[item])
        print(total)
        return(total)

    def getType(self):
        type_list = []
        for item in self.cart_item:
            type_list.append(item.getType())
        print(type_list)
        return(type_list)

    def remove(self, barcode):
        for item in self.cart_item:
            if item.item_barcode == str(barcode):
                self.cart_item.pop(item)
                print(item, "Has been removed !")
                print("In Cart items : ", self.getItem())
                return
        print("Error while remove")

            

    def isExist(self, item_barcode):
        for item in self.cart_item:
            if item.getBarcode() == str(item_barcode):
                print("Duplicate detect at",item)
                return item
        return None

if __name__ == "__main__":
    my_cart = Cart()

    my_item1 = "8850006901656", "โพรเทคส์สบู่ก้อนคอมพลีท12 65กรัม", 15, "ของใช้ภายในบ้าน"
    my_item2 = 8850999321004, "สิงห์น้ำดิ่ม 600cc", 7, "เครื่องดื่ม"

    my_cart.addItem("8850006901656", "โพรเทคส์สบู่ก้อนคอมพลีท12 65กรัม", 15, "ของใช้ภายในบ้าน")
    my_cart.addItem(8850999321004, "สิงห์น้ำดิ่ม 600cc", 7, "เครื่องดื่ม",5)
    my_cart.addItem("8850006901656", "โพรเทคส์สบู่ก้อนคอมพลีท12 65กรัม", 15, "ของใช้ภายในบ้าน")
    my_cart.addItem(8850999321004, "สิงห์น้ำดิ่ม 600cc", 7, "เครื่องดื่ม")
    # my_cart.addItem(8850999321004, "สิงห์น้ำดิ่ม 600cc", 7, "เครื่องดื่ม")
    # my_cart.addItem(8850999321004, "สิงห์น้ำดิ่ม 600cc", 7, "เครื่องดื่ม")

    my_cart.getItem()
    my_cart.getBarcode()
    my_cart.getName()
    my_cart.getPrice()
    my_cart.getCartPrice()
    my_cart.getType()

    my_cart.remove(8850999321004)









