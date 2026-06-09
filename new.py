import flet as ft
from twilio.rest import Client  # 👈 Twilio ଲାଇବ୍ରେରୀ ଆମଦାନୀ ହେଲା

# --- TWILIO CONFIGURATION (ଏଠାରେ ଆପଣଙ୍କ ଡିଟେଲ୍ସ ଲେଖିବେ) ---
# ⚠️ ଆପଣ Twilio ଆକାଉଣ୍ଟ ଖୋଲିଲା ପରେ ଏହି ୩ଟି ଜିନିଷ ବଦଳାଇ ଦେବେ
TWILIO_ACCOUNT_SID = "AC050905cebc925f9e1b60779d66519d39"
TWILIO_AUTH_TOKEN = "eeeaeb1c48b110853c44cffc224bd631"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio ର Sandbox ନମ୍ବର
YOUR_PERSONAL_NUMBER = "whatsapp:+918892535245"   # 👈 ଆପଣଙ୍କ ନିଜ WhatsApp ନମ୍ବର

def send_whatsapp_notification(service, name, mobile, address, req):
    # ଯଦି ଆପଣ Twilio ID ଦେଇନାହାନ୍ତି, ତେବେ ଏହା ଏରର୍ ନଦେଇ ଖାଲି ସ୍କିପ୍ କରିବ
    if "YOUR_" in TWILIO_ACCOUNT_SID:
        print("💡 Note: Twilio credentials not set yet. Skipping WhatsApp send.")
        return
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = (
            f"🚨 *NEW BOOKING RECEIVED!* 🚨\n\n"
            f"🛠️ *Service:* {service}\n"
            f"👤 *Client:* {name}\n"
            f"📞 *Mobile:* {mobile}\n"
            f"📍 *Address:* {address}\n"
            f"📝 *Req:* {req}"
        )
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=YOUR_PERSONAL_NUMBER
        )
        print(f"✅ WhatsApp Notification Sent! SID: {message.sid}")
    except Exception as ex:
        print(f"❌ Failed to send WhatsApp: {ex}")


def main(page: ft.Page):
    page.title = "Krishna Engineering & Home Services"
    page.scroll = "adaptive"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    navbar = ft.AppBar(
        title=ft.Text("🏢 KRISHNA ENGINEERING", weight="bold", color="white", size=22),
        bgcolor="#0F172A", 
    )

    selected_service = ft.Text("", size=16, weight="bold", color="blue")
    client_name = ft.TextField(label="Your Name")
    client_mobile = ft.TextField(label="Mobile Number", keyboard_type=ft.KeyboardType.NUMBER)
    client_address = ft.TextField(label="Full Address", multiline=True, min_lines=2)
    client_req = ft.TextField(label="Specific Requirement", multiline=True, min_lines=2)

    def submit_booking(e):
        if not client_name.value or not client_mobile.value:
            page.overlay.append(ft.SnackBar(ft.Text("⚠️ Please enter Name and Mobile Number!"), open=True))
            page.update()
            return
        
        # ୧. ଟର୍ମିନାଲ୍ ରେ ପ୍ରିଣ୍ଟ ହେବ
        print("\n" + "="*40)
        print("🚨 NEW BOOKING RECEIVED FROM CLIENT! 🚨")
        print(f"🛠️ Service Needed: {selected_service.value}")
        print(f"👤 Client Name: {client_name.value}")
        print(f"📞 Mobile No: {client_mobile.value}")
        print(f"📍 Address: {client_address.value}")
        print(f"📝 Requirement: {client_req.value}")
        print("="*40 + "\n")

        # ୨. 👈 ଏଠାରେ ଆପଣଙ୍କ ମୋବାଇଲ୍ WhatsApp କୁ ମେସେଜ୍ ପଠାଯିବ
        send_whatsapp_notification(
            selected_service.value, 
            client_name.value, 
            client_mobile.value, 
            client_address.value, 
            client_req.value
        )

        page.overlay.append(ft.SnackBar(
            ft.Text(f"🎉 Booking Successful for {selected_service.value}! We will call you soon."),
            open=True
        ))
        
        booking_dialog.open = False
        client_name.value = ""
        client_mobile.value = ""
        client_address.value = ""
        client_req.value = ""
        page.update()

    def close_dialog(e):
        booking_dialog.open = False
        page.update()

    booking_dialog = ft.AlertDialog(
        title=ft.Row([ft.Text("Book Service: "), selected_service]),
        content=ft.Container(
            width=400,
            height=350,
            content=ft.Column([client_name, client_mobile, client_address, client_req], scroll="adaptive")
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.Button("Submit Booking", bgcolor="#1E3A8A", color="white", on_click=submit_booking)
        ],
        actions_alignment="end"
    )

    page.overlay.append(booking_dialog)

    def open_booking_form(e, service_name):
        selected_service.value = service_name
        booking_dialog.open = True
        page.update()

    # --- HERO SECTION ---
    hero_section = ft.Container(
        padding=50,
        gradient=ft.LinearGradient(colors=["#0F172A", "#1E3A8A"]),
        content=ft.Column([
            ft.Text("Home services at your doorstep", size=32, weight="bold", color="white", text_align="center"),
            ft.Text("Expert Professional Engineering & Maintenance Services in Odisha", size=16, color="amber", text_align="center"),
        ], horizontal_alignment="center")
    )

    # --- SERVICES SECTION ---
    def create_service_card(icon_emoji, title_text, desc_text):
        return ft.Card(
            elevation=4,
            content=ft.Container(
                width=220, padding=20, bgcolor="white", border_radius=12,
                content=ft.Column([
                    ft.Text(icon_emoji, size=40), 
                    ft.Container(height=5),
                    ft.Text(title_text, size=18, weight="bold", color="#0F172A"),
                    ft.Text(desc_text, size=13, color="grey"),
                    ft.Container(height=15),
                    ft.TextButton(
                        content=ft.Text("Book Now", color="blue", weight="bold", size=14),
                        on_click=lambda e: open_booking_form(e, title_text)
                    )
                ], horizontal_alignment="center")
            )
        )

    services_grid = ft.Container(
        padding=40, bgcolor="#F8FAFC", 
        content=ft.Column([
            ft.Text("🛠️ OUR EXPERT SERVICES", size=24, weight="bold", color="#0F172A"),
            ft.Container(height=15),
            ft.Row([
                create_service_card("🎨", "Painting", "Interior & Exterior premium wall painting"),
                create_service_card("💧", "Water-Proofing", "Roof, bathroom leakage & damp solutions"),
                create_service_card("⚡", "Electrician", "House wiring, fan, AC repair & installation"),
                create_service_card("🪠", "Plumbing", "Pipe leaks, bathroom fittings & drainage"),
                create_service_card("🪚", "Carpenter", "Furniture repair, doors & modular kitchen"),
            ], wrap=True, spacing=20, alignment="center")
        ])
    )

    # --- ABOUT & CONTACT ---
    about_section = ft.Container(
        padding=40, bgcolor="white",
        content=ft.Column([
            ft.Text("ABOUT OUR COMPANY", size=22, weight="bold", color="#0F172A"),
            ft.Text("Welcome to Krishna Engineering. Inspired by top-tier home service standards...", size=15, color="#334155"),
        ])
    )

    contact_section = ft.Container(
        padding=40, bgcolor="#0F172A", 
        content=ft.Column([
            ft.Text("CONTACT US FOR BOOKINGS", size=22, weight="bold", color="amber"),
            ft.Text("📞 Phone: +91 8892535245", size=16, color="white"),
        ])
    )

    page.add(hero_section, services_grid, about_section, contact_section)

ft.run(main)


