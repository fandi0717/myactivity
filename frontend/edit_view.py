from flet import *
import flet
from reference.ref import RefHalamanTambahJadwal as ref
from reference.ref import RefItemTask as ref2
# from halaman_tambah_jadwal import show_date_picker
# from backend.database import list_of_item
from backend.func import search_by_id as search
from datetime import datetime, timedelta
from reference.ref import RefEditView as ref3
from frontend.tampilan_date_picker import format_date_picker
from backend.format_time import formatted_time
from frontend import item_task


def view_edit_jadwal(page):
    # jadwal = search_by_id(id_task)
    # print(page.controls)
    jadwal = search(ref2.ICON_EDIT.current.data)
    format_jadwal_date = format_date_picker(jadwal.date)
    # page.control.data
    return [
        AppBar(
            title=Text('Edit Jadwal'),
        ),
        Column(
                controls=[
                    TextField(
                        ref=ref3.TEXTFIELD_NAMA_ACARA_EDIT,
                        value=str(jadwal.nama_acara)
                    ),
                    Row(
                        ref=ref3.ROW_DATE_PICKER_EDIT,
                        controls=[
                            IconButton(
                                icon=icons.CALENDAR_MONTH,
                                on_click=lambda e:show_date_picker_edit(e, page, jadwal)
                            ),
                            Container(Text(f"{format_jadwal_date[0]}, {format_jadwal_date[1]} {format_jadwal_date[2]} {format_jadwal_date[3]}"))
                        ],
                        # ref=ref.ROW_DATE_PICKER
                    ),
                    TextField(
                        ref=ref3.TEXTFIELD_WAKTU_EDIT,
                        value=str(jadwal.waktu.strftime('%H:%M'))
                    )
                ]
            ),
            FloatingActionButton(
                text='Setting',
                on_click=lambda e:edit_jadwal(e, page, jadwal)
            )

        
    ]


def show_date_picker_edit(e, page, jadwal):
    DatePicker(
        ref=ref3.DATE_PICKER,
        current_date=jadwal.date,
        first_date=datetime.now(),
        last_date=datetime.now() + timedelta(365),
        on_change=on_change_date_picker_edit
    )

    page.overlay.append(
        ref3.DATE_PICKER.current
    )

    page.add(ref3.DATE_PICKER.current)

    return ref3.DATE_PICKER.current.pick_date()

def on_change_date_picker_edit(e):
    result_format = format_date_picker(ref3.DATE_PICKER.current.value)

    del ref3.ROW_DATE_PICKER_EDIT.current.controls[1]

    ref3.ROW_DATE_PICKER_EDIT.current.controls.append(
        Container(
            Text(f"{result_format[0]}, {result_format[1]} {result_format[2]} {result_format[3]}")
        )
    )

    ref3.ROW_DATE_PICKER_EDIT.current.update()


def edit_jadwal(e, page, jadwal):
    if ref3.DATE_PICKER.current is None:
        res_date = jadwal.date
    else:
        res_date = ref3.DATE_PICKER.current.value


    jadwal.nama_acara = ref3.TEXTFIELD_NAMA_ACARA_EDIT.current.value
    jadwal.date = ref3.DATE_PICKER.current.value if ref3.DATE_PICKER.current is not None else res_date
    jadwal.waktu = formatted_time(ref3.TEXTFIELD_WAKTU_EDIT.current.value)

    page.go("/")

    item_task.show_item_view(page)