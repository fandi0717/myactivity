from flet import *
import flet
from frontend.tampilan_date_picker import format_date_picker
from reference.ref import RefHalamanUtama as ref
from reference.ref import RefItemTask as ref2
from backend import database as db
from backend.func import *
from backend.func import delete_by_id
# from datetime import datetime                     ## WITH DATABASE
# from model.jadwal import Jadwal                   ## WITH DATABASE
# from backend.format_time import formatted_time    ## DENGAN DATABASE



class ItemTask(UserControl):

    def __init__(self, nama_acara, waktu, id_task, datetime, page):
        super().__init__()
        self.nama_acara = nama_acara
        self.waktu = waktu
        self.id = id_task
        self.datetime = datetime
        self.page = page


    def build(self):
        format_datetime_ = format_date_picker(self.datetime)
        return Row(
            controls=[
                Container(
                    content=Card(
                        content=Row(
                            [
                            Text(
                            f'\t\t{self.nama_acara}',
                            weight=FontWeight.BOLD
                        ),
                            ],
                        ), 
                        color=colors.GREEN,
                        height=40,
                    ),
                    # on_click=...,   # self.id
                    expand=4,
                    margin=margin.only(left=20,top=20)


                ),
                Container(
                    content=Card(
                        content=Row(
                            controls=[
                                Text(f"\t\t{format_datetime_[0]}, {format_datetime_[1]} {format_datetime_[2]} {format_datetime_[3]}", weight=FontWeight.BOLD),
                                Text(str(self.waktu.strftime('%H:%M')), weight=FontWeight.BOLD)
                            ]),
                        color=colors.GREEN,
                        height=40
                    ),
                    # on_click=...,   # self.id
                    expand=2,
                    margin=margin.only(top=20)
                ),
                Container(
                    content=IconButton(
                        ref=ref2.ICON_EDIT,
                        icon=icons.EDIT,
                        on_click=lambda e:to_edit_jadwal(e, self.page, self.id),   # self.id
                        tooltip='Edit Jadwal'
                        
                    ),
                    margin=margin.only(top=20)
                ),  
                Container(
                    content=IconButton(
                        icon=icons.DELETE,
                        on_click=lambda e:open_dialog_delete(e, self.page, self.id),   # self.id
                        tooltip='Delete Jadwal'
                    ),
                    margin=margin.only(top=20)
                ),
            ]
        )


def delete_jadwal_dialog(e, page):
    return AlertDialog(
        ref=ref2.ALERT_DIALOG_DELETE,
        title=Text("Peringatan"),
        content=Text("Apakah Anda yakin ingin menghapus Jadwal ini ?"),
        actions=[
            TextButton(
                text='Batal',
                on_click=lambda e:close_dialog_delete(e, page)
            ),
            TextButton(
                text='Hapus',
                on_click=lambda e:click_hapus_delete(page)
            )
        ],
        actions_alignment=MainAxisAlignment.SPACE_AROUND,
    )


def click_hapus_delete(page):
    data_now = ref2.ALERT_DIALOG_DELETE.current.data
    print(data_now)
    jadwal = search_by_id(data_now)
    close_dialog_delete(object(), page)
    delete_by_id(data_now)

    for x in ref.LISTVIEW.current.controls:
        print(type(x))
        if x.id == data_now:
            print(f'id:{x.id} | {data_now}')
            ref.LISTVIEW.current.controls.remove(x)
            print(f'List : {ref.LISTVIEW.current.controls}')
        ref.LISTVIEW.current.update()
    print(list_of_item)
    # show_item_view(page)

def open_dialog_delete(e, page, id_task):
    # page.dialog = ref2.ALERT_DIALOG_DELETE.current
    page.dialog = delete_jadwal_dialog(object(), page)
    ref2.ALERT_DIALOG_DELETE.current.open = True
    ref2.ALERT_DIALOG_DELETE.current.data = id_task
    page.update()

def close_dialog_delete(e, page):
    ref2.ALERT_DIALOG_DELETE.current.open = False
    page.update()



def to_edit_jadwal(e, page, id_task):
    ref2.ICON_EDIT.current.data = id_task
    page.go('/edit_jadwal')

def show_item_view(page):
    #### WITH DATABASE
    # if len(db.object_db.get_all_data()) != 0:
    #     for data in db.object_db.get_all_data():
    #         db.list_of_item.append(
    #             Jadwal(
    #                 data['id'],
    #                 data['nama_jadwal'],
    #                 datetime.strptime(data['tanggal'], '%Y-%m-%d'),
    #                 formatted_time(data['waktu'])
    #             )
    #         )
    #     # for jadwal in db.list_of_item]:   # terbary dari bawah ke atas
    #     for jadwal in db.list_of_item[::-1]:    # terbaru dari atas ke bawah
    #         ref.LISTVIEW.current.controls.append(
    #             ItemTask(
    #                 jadwal.nama_acara, 
    #                 jadwal.waktu, 
    #                 jadwal.id, 
    #                 jadwal.date,
    #                 page
    #             )
    #         )
    #     if ref.LISTVIEW.current is not None:
    #         ref.LISTVIEW.current.update()

    ##### NO DATABASE
    # for jadwal in db.list_of_item]:   # terbary dari bawah ke atas
    for jadwal in db.list_of_item[::-1]:    # terbaru dari atas ke bawah
        ref.LISTVIEW.current.controls.append(
            ItemTask(
                jadwal.nama_acara, 
                jadwal.waktu, 
                jadwal.id, 
                jadwal.date,
                page
            )
        )
    if ref.LISTVIEW.current is not None:
        ref.LISTVIEW.current.update()
