import json
import random

def generate_menu():
    """Generate a comprehensive Vietnamese restaurant menu with 50+ dishes"""
    
    menu = []
    
    # Món chính - Main dishes (20 items)
    main_dishes = [
        {
            "id": "P001",
            "name": "Phở Bò",
            "category": "Món chính",
            "price": 45000,
            "description": "Phở bò truyền thống Hà Nội với nước dùng hầm xương 12 tiếng, thịt bò tươi mềm",
            "ingredients": ["Bánh phở", "Thịt bò", "Hành lá", "Ngò rí"],
            "available": True
        },
        {
            "id": "P002",
            "name": "Phở Gà",
            "category": "Món chính",
            "price": 40000,
            "description": "Phở gà thanh đạm với nước dùng từ xương gà và thịt gà luộc mềm",
            "ingredients": ["Bánh phở", "Thịt gà", "Hành lá", "Ngò rí"],
            "available": True
        },
        {
            "id": "P003",
            "name": "Bún Bò Huế",
            "category": "Món chính",
            "price": 50000,
            "description": "Bún bò Huế cay nồng, nước dùng đậm đà với sả và mắm ruốc",
            "ingredients": ["Bún bò", "Thịt bò", "Chả", "Sả", "Mắm ruốc"],
            "available": True
        },
        {
            "id": "P004",
            "name": "Bún Chả Hà Nội",
            "category": "Món chính",
            "price": 50000,
            "description": "Bún chả Hà Nội với thịt nướng thơm, nước mắm chua ngọt đặc trưng",
            "ingredients": ["Bún tươi", "Thịt nướng", "Chả viên", "Nước mắm"],
            "available": True
        },
        {
            "id": "P005",
            "name": "Bún Riêu Cua",
            "category": "Món chính",
            "price": 45000,
            "description": "Bún riêu với nước dùng cà chua chua chua, riêu cua thơm ngon",
            "ingredients": ["Bún", "Riêu cua", "Cà chua", "Đậu hũ"],
            "available": True
        },
        {
            "id": "P006",
            "name": "Cơm Gà Xối Mỡ",
            "category": "Món chính",
            "price": 40000,
            "description": "Cơm gà Hải Nam với gà luộc mềm, cơm thơm bơ",
            "ingredients": ["Cơm", "Gà luộc", "Nước sốt gừng", "Dưa leo"],
            "available": True
        },
        {
            "id": "P007",
            "name": "Cơm Tấm Sườn",
            "category": "Món chính",
            "price": 45000,
            "description": "Cơm tấm Sài Gòn với sườn nướng, trứng ốp la, bì",
            "ingredients": ["Cơm tấm", "Sườn nướng", "Trứng", "Bì"],
            "available": True
        },
        {
            "id": "P008",
            "name": "Cơm Gà Nướng",
            "category": "Món chính",
            "price": 42000,
            "description": "Cơm gà nướng mật ong thơm phức, gà mềm ngọt",
            "ingredients": ["Cơm", "Gà nướng", "Mật ong", "Salad"],
            "available": True
        },
        {
            "id": "P009",
            "name": "Hủ Tiếu Nam Vang",
            "category": "Món chính",
            "price": 45000,
            "description": "Hủ tiếu Nam Vang với tôm, thịt, gan, nước dùng ngọt thanh",
            "ingredients": ["Hủ tiếu", "Tôm", "Thịt", "Gan", "Hành tím"],
            "available": True
        },
        {
            "id": "P010",
            "name": "Mì Quảng",
            "category": "Món chính",
            "price": 48000,
            "description": "Mì Quảng đặc sản miền Trung với tôm, thịt và nước dùng đậm đà",
            "ingredients": ["Mì Quảng", "Tôm", "Thịt", "Đậu phộng", "Rau sống"],
            "available": True
        },
        {
            "id": "P011",
            "name": "Bánh Mì Thịt",
            "category": "Món chính",
            "price": 25000,
            "description": "Bánh mì Sài Gòn giòn tan với pate, thịt nguội, dưa leo",
            "ingredients": ["Bánh mì", "Pate", "Thịt nguội", "Dưa leo", "Rau"],
            "available": True
        },
        {
            "id": "P012",
            "name": "Bánh Mì Xíu Mại",
            "category": "Món chính",
            "price": 28000,
            "description": "Bánh mì xíu mại sốt cà chua đậm đà",
            "ingredients": ["Bánh mì", "Xíu mại", "Sốt cà chua"],
            "available": True
        },
        {
            "id": "P013",
            "name": "Cao Lầu",
            "category": "Món chính",
            "price": 45000,
            "description": "Cao lầu Hội An với sợi mì dai, thịt xá xíu và rau thơm",
            "ingredients": ["Mì cao lầu", "Xá xíu", "Rau", "Bánh đa"],
            "available": True
        },
        {
            "id": "P014",
            "name": "Bún Mắm",
            "category": "Món chính",
            "price": 50000,
            "description": "Bún mắm miền Tây với cá lóc, tôm và nước mắm đặc trưng",
            "ingredients": ["Bún", "Cá lóc", "Tôm", "Mắm", "Rau"],
            "available": True
        },
        {
            "id": "P015",
            "name": "Bánh Canh Cua",
            "category": "Món chính",
            "price": 45000,
            "description": "Bánh canh cua với sợi bánh dai, nước dùng ngọt từ cua",
            "ingredients": ["Bánh canh", "Cua", "Chả cá", "Hành lá"],
            "available": True
        },
        {
            "id": "P016",
            "name": "Cơm Chiên Dương Châu",
            "category": "Món chính",
            "price": 42000,
            "description": "Cơm chiên Dương Châu với tôm, xúc xích, trứng",
            "ingredients": ["Cơm", "Tôm", "Xúc xích", "Trứng", "Đậu Hà Lan"],
            "available": True
        },
        {
            "id": "P017",
            "name": "Mì Xào Giòn",
            "category": "Món chính",
            "price": 48000,
            "description": "Mì xào giòn với hải sản và rau củ thập cẩm",
            "ingredients": ["Mì", "Tôm", "Mực", "Rau củ"],
            "available": True
        },
        {
            "id": "P018",
            "name": "Bún Đậu Mắm Tôm",
            "category": "Món chính",
            "price": 45000,
            "description": "Bún đậu mắm tôm với thịt luộc, chả cốm và mắm tôm đặc trưng",
            "ingredients": ["Bún", "Đậu hũ chiên", "Thịt", "Chả cốm", "Mắm tôm"],
            "available": True
        },
        {
            "id": "P019",
            "name": "Lẩu Thái",
            "category": "Món chính",
            "price": 180000,
            "description": "Lẩu Thái chua cay với tôm, mực, nấm và rau (phục vụ 2-3 người)",
            "ingredients": ["Tôm", "Mực", "Nấm", "Rau", "Nước lẩu Thái"],
            "available": True
        },
        {
            "id": "P020",
            "name": "Lẩu Bò Nhúng Dấm",
            "category": "Món chính",
            "price": 200000,
            "description": "Lẩu bò nhúng dấm chua ngọt đặc trưng (phục vụ 2-3 người)",
            "ingredients": ["Bò", "Rau", "Nấm", "Nước dấm"],
            "available": True
        }
    ]
    
    # Khai vị - Appetizers (10 items)
    appetizers = [
        {
            "id": "A001",
            "name": "Gỏi Cuốn",
            "category": "Khai vị",
            "price": 30000,
            "description": "Gỏi cuốn tôm thịt tươi ngon với rau sống và nước chấm đậu phộng",
            "ingredients": ["Bánh tráng", "Tôm", "Thịt", "Rau sống", "Bún"],
            "available": True
        },
        {
            "id": "A002",
            "name": "Chả Giò",
            "category": "Khai vị",
            "price": 35000,
            "description": "Chả giò chiên giòn với nhân thịt và rau củ",
            "ingredients": ["Bánh đa nem", "Thịt", "Miến", "Rau củ"],
            "available": True
        },
        {
            "id": "A003",
            "name": "Nem Nướng",
            "category": "Khai vị",
            "price": 40000,
            "description": "Nem nướng Nha Trang thơm phức, ăn kèm bánh tráng và rau",
            "ingredients": ["Thịt lợn", "Tỏi", "Rau", "Bánh tráng"],
            "available": True
        },
        {
            "id": "A004",
            "name": "Gỏi Ngó Sen",
            "category": "Khai vị",
            "price": 45000,
            "description": "Gỏi ngó sen tôm thịt thanh mát, giòn ngon",
            "ingredients": ["Ngó sen", "Tôm", "Thịt", "Rau răm"],
            "available": True
        },
        {
            "id": "A005",
            "name": "Gỏi Gà",
            "category": "Khai vị",
            "price": 42000,
            "description": "Gỏi gà bắp cải chua ngọt đặc trưng",
            "ingredients": ["Thịt gà", "Bắp cải", "Cà rốt", "Rau răm"],
            "available": True
        },
        {
            "id": "A006",
            "name": "Khoai Tây Chiên",
            "category": "Khai vị",
            "price": 25000,
            "description": "Khoai tây chiên giòn tan, ăn kèm tương ớt",
            "ingredients": ["Khoai tây", "Muối", "Tương ớt"],
            "available": True
        },
        {
            "id": "A007",
            "name": "Cánh Gà Chiên Nước Mắm",
            "category": "Khai vị",
            "price": 45000,
            "description": "Cánh gà chiên nước mắm thơm phức, giòn rụm",
            "ingredients": ["Cánh gà", "Nước mắm", "Tỏi"],
            "available": True
        },
        {
            "id": "A008",
            "name": "Đậu Hũ Chiên",
            "category": "Khai vị",
            "price": 30000,
            "description": "Đậu hũ chiên giòn, ăn kèm nước chấm",
            "ingredients": ["Đậu hũ", "Hành lá"],
            "available": True
        },
        {
            "id": "A009",
            "name": "Bò Bía",
            "category": "Khai vị",
            "price": 35000,
            "description": "Bò bía cuốn tươi với rau, trứng và nước chấm ngọt",
            "ingredients": ["Bánh tráng", "Rau", "Trứng", "Xúc xích"],
            "available": True
        },
        {
            "id": "A010",
            "name": "Súp Cua",
            "category": "Khai vị",
            "price": 38000,
            "description": "Súp cua đặc sánh, thơm ngon",
            "ingredients": ["Cua", "Ngô", "Trứng", "Nấm"],
            "available": True
        }
    ]
    
    # Đồ uống - Beverages (15 items)
    beverages = [
        {
            "id": "D001",
            "name": "Trà Đá",
            "category": "Đồ uống",
            "price": 5000,
            "description": "Trà đá truyền thống, giải khát mát lạnh",
            "ingredients": ["Trà", "Đá"],
            "available": True
        },
        {
            "id": "D002",
            "name": "Nước Chanh",
            "category": "Đồ uống",
            "price": 15000,
            "description": "Nước chanh tươi vắt, ngọt vừa phải",
            "ingredients": ["Chanh", "Đường", "Đá"],
            "available": True
        },
        {
            "id": "D003",
            "name": "Cà Phê Sữa Đá",
            "category": "Đồ uống",
            "price": 20000,
            "description": "Cà phê phin truyền thống pha sữa đặc, đá mát",
            "ingredients": ["Cà phê", "Sữa đặc", "Đá"],
            "available": True
        },
        {
            "id": "D004",
            "name": "Cà Phê Đen",
            "category": "Đồ uống",
            "price": 18000,
            "description": "Cà phê đen đậm đà, thơm nồng",
            "ingredients": ["Cà phê", "Đá"],
            "available": True
        },
        {
            "id": "D005",
            "name": "Nước Dừa",
            "category": "Đồ uống",
            "price": 20000,
            "description": "Nước dừa tươi mát lạnh, ngọt tự nhiên",
            "ingredients": ["Dừa tươi"],
            "available": True
        },
        {
            "id": "D006",
            "name": "Sinh Tố Bơ",
            "category": "Đồ uống",
            "price": 30000,
            "description": "Sinh tố bơ béo ngậy, thơm ngon",
            "ingredients": ["Bơ", "Sữa đặc", "Đá"],
            "available": True
        },
        {
            "id": "D007",
            "name": "Sinh Tố Dâu",
            "category": "Đồ uống",
            "price": 32000,
            "description": "Sinh tố dâu tươi, chua ngọt vừa phải",
            "ingredients": ["Dâu tây", "Sữa chua", "Đường"],
            "available": True
        },
        {
            "id": "D008",
            "name": "Trà Sữa Trân Châu",
            "category": "Đồ uống",
            "price": 35000,
            "description": "Trà sữa trân châu đường đen thơm ngon",
            "ingredients": ["Trà", "Sữa", "Trân châu"],
            "available": True
        },
        {
            "id": "D009",
            "name": "Nước Cam Vắt",
            "category": "Đồ uống",
            "price": 25000,
            "description": "Nước cam tươi vắt, giàu vitamin C",
            "ingredients": ["Cam", "Đường"],
            "available": True
        },
        {
            "id": "D010",
            "name": "Soda Chanh",
            "category": "Đồ uống",
            "price": 22000,
            "description": "Soda chanh sảng khoái, giải nhiệt",
            "ingredients": ["Soda", "Chanh", "Đường"],
            "available": True
        },
        {
            "id": "D011",
            "name": "Trà Atiso",
            "category": "Đồ uống",
            "price": 18000,
            "description": "Trá atiso giải nhiệt, mát gan",
            "ingredients": ["Atiso", "Đường"],
            "available": True
        },
        {
            "id": "D012",
            "name": "Nước Mía",
            "category": "Đồ uống",
            "price": 15000,
            "description": "Nước mía tươi ngọt mát",
            "ingredients": ["Mía", "Đá", "Chanh"],
            "available": True
        },
        {
            "id": "D013",
            "name": "Sữa Tươi",
            "category": "Đồ uống",
            "price": 20000,
            "description": "Sữa tươi nguyên chất, bổ dưỡng",
            "ingredients": ["Sữa tươi"],
            "available": True
        },
        {
            "id": "D014",
            "name": "Trà Đào Cam Sả",
            "category": "Đồ uống",
            "price": 35000,
            "description": "Trà đào cam sả thanh mát, thơm dịu",
            "ingredients": ["Trà", "Đào", "Cam", "Sả"],
            "available": True
        },
        {
            "id": "D015",
            "name": "Bia Sài Gòn",
            "category": "Đồ uống",
            "price": 25000,
            "description": "Bia Sài Gòn chai lạnh",
            "ingredients": ["Bia"],
            "available": True
        }
    ]
    
    # Tráng miệng - Desserts (10 items)
    desserts = [
        {
            "id": "T001",
            "name": "Chè Thái",
            "category": "Tráng miệng",
            "price": 25000,
            "description": "Chè Thái với nhiều loại trái cây và nước cốt dừa",
            "ingredients": ["Thạch", "Trái cây", "Nước cốt dừa", "Đá bào"],
            "available": True
        },
        {
            "id": "T002",
            "name": "Chè Ba Màu",
            "category": "Tráng miệng",
            "price": 22000,
            "description": "Chè ba màu truyền thống với đậu đỏ, đậu xanh và thạch",
            "ingredients": ["Đậu đỏ", "Đậu xanh", "Thạch", "Nước cốt dừa"],
            "available": True
        },
        {
            "id": "T003",
            "name": "Kem Flan",
            "category": "Tráng miệng",
            "price": 20000,
            "description": "Kem flan mát lạnh, béo ngậy với caramel thơm",
            "ingredients": ["Trứng", "Sữa", "Caramel"],
            "available": True
        },
        {
            "id": "T004",
            "name": "Chè Bưởi",
            "category": "Tráng miệng",
            "price": 25000,
            "description": "Chè bưởi thanh mát với nước cốt dừa",
            "ingredients": ["Bưởi", "Nước cốt dừa", "Đường"],
            "available": True
        },
        {
            "id": "T005",
            "name": "Sương Sa Hạt Lựu",
            "category": "Tráng miệng",
            "price": 28000,
            "description": "Sương sa hạt lựu mát lạnh, ngọt dịu",
            "ingredients": ["Sương sa", "Hạt lựu", "Nước cốt dừa"],
            "available": True
        },
        {
            "id": "T006",
            "name": "Rau Câu",
            "category": "Tráng miệng",
            "price": 18000,
            "description": "Rau câu nhiều màu sắc, thơm mát",
            "ingredients": ["Rau câu", "Nước dừa", "Đường"],
            "available": True
        },
        {
            "id": "T007",
            "name": "Yaourt Dẻo",
            "category": "Tráng miệng",
            "price": 15000,
            "description": "Yaourt dẻo mịn, chua ngọt vừa phải",
            "ingredients": ["Sữa chua", "Đường"],
            "available": True
        },
        {
            "id": "T008",
            "name": "Chè Đậu Đỏ",
            "category": "Tráng miệng",
            "price": 20000,
            "description": "Chè đậu đỏ nóng, ngọt bùi",
            "ingredients": ["Đậu đỏ", "Đường", "Nước cốt dừa"],
            "available": True
        },
        {
            "id": "T009",
            "name": "Bánh Flan",
            "category": "Tráng miệng",
            "price": 18000,
            "description": "Bánh flan mềm mịn, caramel đắng dịu",
            "ingredients": ["Trứng", "Sữa", "Đường caramel"],
            "available": True
        },
        {
            "id": "T010",
            "name": "Chè Chuối",
            "category": "Tráng miệng",
            "price": 22000,
            "description": "Chè chuối nóng với nước cốt dừa thơm béo",
            "ingredients": ["Chuối", "Bột sắn", "Nước cốt dừa"],
            "available": True
        }
    ]
    
    # Combine all items
    menu.extend(main_dishes)
    menu.extend(appetizers)
    menu.extend(beverages)
    menu.extend(desserts)
    
    return menu

def save_menu(menu, filename="data/menu.json"):
    """Save menu to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)
    print(f"✓ Menu with {len(menu)} dishes saved to {filename}")

def print_menu_summary(menu):
    """Print menu summary by category"""
    categories = {}
    for item in menu:
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    print("\n" + "="*60)
    print("MENU SUMMARY")
    print("="*60)
    
    for category, items in categories.items():
        print(f"\n{category.upper()} ({len(items)} items):")
        for item in items:
            print(f"  • {item['name']:<30} {item['price']:>8,}đ")
    
    total_items = len(menu)
    avg_price = sum(item['price'] for item in menu) / total_items
    print("\n" + "="*60)
    print(f"Total dishes: {total_items}")
    print(f"Average price: {avg_price:,.0f}đ")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Generate menu
    menu = generate_menu()
    
    # Save to file
    save_menu(menu)
    
    # Print summary
    print_menu_summary(menu)
