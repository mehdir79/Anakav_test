import pymysql
from sqlalchemy import String , ForeignKey , event  , select , func , create_engine
from sqlalchemy.orm import DeclarativeBase ,Mapped , mapped_column , Session , Relationship , sessionmaker ,scoped_session

from sqlalchemy import select, func , UniqueConstraint
from sqlalchemy.orm import Session

def update_majmo_row(connection, city_name, year, month):
    session = Session(bind=connection)
    with session.no_autoflush:
        def get_sum(model, column):
            return session.scalar(
                select(func.coalesce(func.sum(column), 0)).where(
                    model.city_name == city_name,
                    model.year == year,
                    model.month == month
                )
            ) or 0

        row = session.query(majmo).filter_by(
            city_name=city_name,
            year=year,
            month=month
        ).first()

        if not row:
            row = majmo(city_name=city_name, year=year, month=month,
                        dardast_ejra = sum(get_sum(m, m.dardast_ejra) or 0 for m in [test1, test2, test3, test4, test5, test6, test7]),
                        tahie_soorat_vaziat = sum(get_sum(m, m.tahie_soorat_vaziat) or 0  for m in [test1, test2, test3, test4, test5, test6, test7]),
                        soorat_vaziat_moshaver = sum(get_sum(m, getattr(m, 'soorat_vaziat_moshaver', 0)) or 0  for m in [test4, test5, test6, test7]),
                        soorat_vaziat_setad = sum(get_sum(m, m.soorat_vaziat_setad) or 0  for m in [test1, test2, test3, test4, test5, test6, test7]),
                        soorat_vaziat_mali = sum(get_sum(m, m.soorat_vaziat_mali) or 0  for m in [test1, test2, test3, test4, test5, test6, test7]))
            row.majmo_kol = (
                row.dardast_ejra +
                row.tahie_soorat_vaziat +
                row.soorat_vaziat_moshaver +
                row.soorat_vaziat_setad +
                row.soorat_vaziat_mali
            )
            session.add(row)
            session.commit()
        else:
            row.dardast_ejra = sum(get_sum(m, m.dardast_ejra) for m in [test1, test2, test3, test4, test5, test6, test7])
            row.tahie_soorat_vaziat = sum(get_sum(m, m.tahie_soorat_vaziat)for m in [test1, test2, test3, test4, test5, test6, test7])
            row.soorat_vaziat_moshaver = sum(get_sum(m, getattr(m, 'soorat_vaziat_moshaver', 0)) for m in [test4, test5, test6, test7])
            row.soorat_vaziat_setad = sum(get_sum(m, m.soorat_vaziat_setad) for m in [test1, test2, test3, test4, test5, test6, test7])
            row.soorat_vaziat_mali = sum(get_sum(m, m.soorat_vaziat_mali) for m in [test1, test2, test3, test4, test5, test6, test7])

            row.majmo_kol = (
                row.dardast_ejra +
                row.tahie_soorat_vaziat +
                row.soorat_vaziat_moshaver +
                row.soorat_vaziat_setad +
                row.soorat_vaziat_mali
            )
            session.commit()
        session.close()



class Base(DeclarativeBase):
    pass




class cities(Base):
    __tablename__ = "مدیریت برق شهرستان"

    city_id : Mapped[int] = mapped_column( "آیدی شهر" ,key="city_id" ,  autoincrement=True , primary_key= True , unique= True)
    name : Mapped[str] = mapped_column("نام شهر",String(50), key = "name" , unique=True )
    code_omor : Mapped[int] = mapped_column("کد امور" ,key = "code_omor" ,  unique=True  )    

    test1_items = Relationship("test1", back_populates="city")
    test2_items = Relationship("test2", back_populates="city")
    test3_items = Relationship("test3", back_populates="city")
    test4_items = Relationship("test4", back_populates="city")
    test5_items = Relationship("test5", back_populates="city")
    test6_items = Relationship("test6", back_populates="city")
    test7_items = Relationship("test7", back_populates="city")
    majmo_items = Relationship("majmo", back_populates="city")

    def __init__(self , name , code_omor):
        self.name = name
        self.code_omor = code_omor



class test1(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 1"
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True ,unique=True , primary_key=True, key = "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name",onupdate="CASCADE", ondelete="CASCADE"), key = "city_name")
    year : Mapped[int] = mapped_column("سال" , key = "year")
    month : Mapped[int] = mapped_column("ماه",key = "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا"  ,key = "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت",key = "tahie_soorat_vaziat")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد" , key = "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی" , key = "soorat_vaziat_mali" )
    majmo_test1:Mapped[int] = mapped_column('مجموع دستورکارهای باز بهره برداری' , key = "majmo_test1" )

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test1_items")
    


    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test1 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_setad + soorat_vaziat_mali)
        
@event.listens_for(test1, "before_insert")
@event.listens_for(test1, "before_update")
def update_majmo_test1(mapper, connection, target):
    target.majmo_test1 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_setad + target.soorat_vaziat_mali)


@event.listens_for(test1, "after_insert")
@event.listens_for(test1, "after_update")
@event.listens_for(test1, "after_delete")
def handle_test1_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )


class test2(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 2"
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True,unique=True , primary_key=True, key = "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name" ,onupdate="CASCADE", ondelete="CASCADE") , key = "city_name")
    year : Mapped[int] = mapped_column("سال", key = "year")
    month : Mapped[int] = mapped_column("ماه" , key = "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا" , key = "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت", key = "tahie_soorat_vaziat")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد", key = "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    majmo_test2 : Mapped[int] = mapped_column('مجموع دستورکارهای باز لوازم اندازه گیری' ,key= "majmo_test2")

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test2_items")


    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test2 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_setad + soorat_vaziat_mali)

@event.listens_for(test2, "before_insert")
@event.listens_for(test2, "before_update")
def update_majmo_test2(mapper, connection, target):
    target.majmo_test2 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_setad + target.soorat_vaziat_mali) 


@event.listens_for(test2, "after_insert")
@event.listens_for(test2, "after_update")
@event.listens_for(test2, "after_delete")
def handle_test2_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )


class test3(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 3"
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True,unique=True , primary_key=True ,key= "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name" ,onupdate="CASCADE", ondelete="CASCADE") ,key= "city_name")
    year : Mapped[int] = mapped_column("سال",key= "year")
    month : Mapped[int] = mapped_column("ماه" ,key= "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا",key= "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت" ,key= "tahie_soorat_vaziat")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد",key= "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    majmo_test3 : Mapped[int] = mapped_column('مجموع دستورکارهای باز لوازم اندازه گیری',key= "majmo_test3")

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test3_items")
    
    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test3 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_setad + soorat_vaziat_mali)

@event.listens_for(test3, "before_insert")
@event.listens_for(test3, "before_update")
def update_majmo_test3(mapper, connection, target):
    target.majmo_test3 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_setad + target.soorat_vaziat_mali)


@event.listens_for(test3, "after_insert")
@event.listens_for(test3, "after_update")
@event.listens_for(test3, "after_delete")
def handle_test3_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )


class test4(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 4"
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True,unique=True , primary_key=True,key= "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name" ,onupdate="CASCADE", ondelete="CASCADE"),key= "city_name")
    year : Mapped[int] = mapped_column("سال",key= "year")
    month : Mapped[int] = mapped_column("ماه",key= "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا",key= "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت",key= "tahie_soorat_vaziat")
    soorat_vaziat_moshaver : Mapped[int] = mapped_column("صورت وضعیت نزد مشاور",key= "soorat_vaziat_moshaver")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد",key= "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    majmo_test4 : Mapped[int] = mapped_column('مجموع دستورکارهای باز سیم به کابل',key= "majmo_test4")

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test4_items")

    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat, soorat_vaziat_moshaver,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_moshaver = soorat_vaziat_moshaver
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test4 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_moshaver + soorat_vaziat_setad + soorat_vaziat_mali)

@event.listens_for(test4, "before_insert")
@event.listens_for(test4, "before_update")
def update_majmo_test4(mapper, connection, target):
    target.majmo_test4 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_moshaver +  target.soorat_vaziat_setad + target.soorat_vaziat_mali)


@event.listens_for(test4, "after_insert")
@event.listens_for(test4, "after_update")
@event.listens_for(test4, "after_delete")
def handle_test4_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )
     
class test5(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 5"
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True,unique=True , primary_key=True,key= "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name" ,onupdate="CASCADE", ondelete="CASCADE"),key= "city_name")
    year : Mapped[int] = mapped_column("سال",key= "year")
    month : Mapped[int] = mapped_column("ماه",key= "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا",key= "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت",key= "tahie_soorat_vaziat")
    soorat_vaziat_moshaver : Mapped[int] = mapped_column("صورت وضعیت نزد مشاور",key= "soorat_vaziat_moshaver")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد",key= "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    majmo_test5 : Mapped[int] = mapped_column('مجموع دستورکارهای باز نیرورسانی',key= "majmo_test5")

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test5_items")

    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat, soorat_vaziat_moshaver,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_moshaver = soorat_vaziat_moshaver
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test5 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_moshaver + soorat_vaziat_setad + soorat_vaziat_mali)

@event.listens_for(test5, "before_insert")
@event.listens_for(test5, "before_update")
def update_majmo_test5(mapper, connection, target):
    target.majmo_test5 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_moshaver +  target.soorat_vaziat_setad + target.soorat_vaziat_mali)



@event.listens_for(test5, "after_insert")
@event.listens_for(test5, "after_update")
@event.listens_for(test5, "after_delete")
def handle_test5_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )

class test6(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 6"
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True,unique=True , primary_key=True,key= "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name",onupdate="CASCADE" , ondelete="CASCADE"),key= "city_name")
    year : Mapped[int] = mapped_column("سال",key= "year")
    month : Mapped[int] = mapped_column("ماه",key= "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا",key= "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت",key= "tahie_soorat_vaziat")
    soorat_vaziat_moshaver : Mapped[int] = mapped_column("صورت وضعیت نزد مشاور",key= "soorat_vaziat_moshaver")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد",key= "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    majmo_test6 : Mapped[int] = mapped_column('مجموع دستورکارهای باز تلفات',key= "majmo_test6")

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test6_items")

    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat, soorat_vaziat_moshaver,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_moshaver = soorat_vaziat_moshaver
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test6 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_moshaver + soorat_vaziat_setad + soorat_vaziat_mali)


@event.listens_for(test6, "before_insert")
@event.listens_for(test6, "before_update")
def update_majmo_test6(mapper, connection, target):
    target.majmo_test6 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_moshaver +  target.soorat_vaziat_setad + target.soorat_vaziat_mali)



@event.listens_for(test6, "after_insert")
@event.listens_for(test6, "after_update")
@event.listens_for(test6, "after_delete")
def handle_test6_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )


class test7(Base):
    __tablename__ = "تعداد دستورکارهای باز مربوط به تست 7"
    
    test_id :Mapped[int]= mapped_column("آیدی" , autoincrement=True,unique=True , primary_key=True,key= "test_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name" ,onupdate="CASCADE", ondelete="CASCADE"),key= "city_name")
    year : Mapped[int] = mapped_column("سال",key= "year")
    month : Mapped[int] = mapped_column("ماه",key= "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا",key= "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت",key= "tahie_soorat_vaziat")
    soorat_vaziat_moshaver : Mapped[int] = mapped_column("صورت وضعیت نزد مشاور",key= "soorat_vaziat_moshaver")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد",key= "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    key = 'مجموع دستورکارهای باز توسعه و احداث و اصلاح و روشنایی معابر و برگشتی و طرح جامع بم'
    majmo_test7 : Mapped[int] = mapped_column("majmo_test_7",key= "majmo_test7")

    __table_args__ = (
        UniqueConstraint("city_name", "year", "month", name="uq_city_year_month"),
    )

    city = Relationship("cities", back_populates="test7_items")

    def __init__(self , city_name , year , month , dardast_ejra,tahie_soorat_vaziat, soorat_vaziat_moshaver,soorat_vaziat_setad ,soorat_vaziat_mali):
        self.city_name = city_name
        self.year = year
        self.month = month
        self.dardast_ejra = dardast_ejra
        self.tahie_soorat_vaziat = tahie_soorat_vaziat
        self.soorat_vaziat_moshaver = soorat_vaziat_moshaver
        self.soorat_vaziat_setad = soorat_vaziat_setad
        self.soorat_vaziat_mali = soorat_vaziat_mali
        self.majmo_test7 = (dardast_ejra + tahie_soorat_vaziat + soorat_vaziat_moshaver + soorat_vaziat_setad + soorat_vaziat_mali)




@event.listens_for(test7, "before_insert")
@event.listens_for(test7, "before_update")
def update_majmo_test7(mapper, connection, target):
    target.majmo_test7 = (target.dardast_ejra + target.tahie_soorat_vaziat + target.soorat_vaziat_moshaver +  target.soorat_vaziat_setad + target.soorat_vaziat_mali)


@event.listens_for(test7, "after_insert")
@event.listens_for(test7, "after_update")
@event.listens_for(test7, "after_delete")
def handle_test7_event(mapper, connection, target):
    update_majmo_row(
        connection=connection,
        city_name=target.city_name,
        year=target.year,
        month=target.month
    )

        

class majmo(Base):
    __tablename__ = 'جمع تعداد دستورکارهای باز مربوط به امور'
    jam_id :Mapped[int] = mapped_column("آیدی",primary_key=True , autoincrement=True,unique=True,key= "jam_id")
    city_name : Mapped[int] = mapped_column("نام شهر" , ForeignKey("مدیریت برق شهرستان.name" ,onupdate="CASCADE", ondelete="CASCADE"),key= "city_name")
    year : Mapped[int] = mapped_column("سال",key= "year")
    month : Mapped[int] = mapped_column("ماه",key= "month")
    dardast_ejra : Mapped[int] = mapped_column("دردست اجرا",key= "dardast_ejra")    
    tahie_soorat_vaziat : Mapped[int] = mapped_column("تهیه صورت وضعیت",key= "tahie_soorat_vaziat")
    soorat_vaziat_moshaver : Mapped[int] = mapped_column("صورت وضعیت نزد مشاور",key= "soorat_vaziat_moshaver")
    soorat_vaziat_setad : Mapped[int] = mapped_column("صورت وضعیت نزد ستاد",key= "soorat_vaziat_setad")
    soorat_vaziat_mali : Mapped[int] = mapped_column("صورت وضعیت نزد مالی",key= "soorat_vaziat_mali")
    majmo_kol : Mapped[int] = mapped_column('کل دستورکارهای باز',key= "majmo_kol")

    city = Relationship("cities", back_populates="majmo_items")


from sqlalchemy import create_engine
# engine = create_engine("mysql+pymysql://root:1234@localhost/test")
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(bind=engine)
