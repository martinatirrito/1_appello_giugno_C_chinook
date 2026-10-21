from database.DB_connect import DBConnect
from model.arco import Arco
from model.artist import Artist


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select a.*, count(distinct t.TrackId ) as listaBrani, count(distinct pt.PlaylistId) as playlist
                    from Artist a, Album al, Track t, PlaylistTrack pt 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId  and t.TrackId = pt.TrackId 
                    group by a.ArtistId"""

        cursor.execute(query, )

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    def getAllEdges(idMapA):
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select a1.ArtistId as a1, a2.ArtistId as a2, count(distinct a1.PlaylistId) as peso 
                    from (select distinct a.ArtistId,  pt.PlaylistId 
                            from Artist a, Album al, Track t, PlaylistTrack pt
                            where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.TrackId = pt.TrackId) a1, 
                            (select distinct a.ArtistId, pt.PlaylistId 
                                from Artist a, Album al, Track t, PlaylistTrack pt
                                where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.TrackId = pt.TrackId)	a2
                    where a1.ArtistId < a2.ArtistId 
                    and a1.PlaylistId = a2.PlaylistId 
                    group by a1.ArtistId, a2.ArtistId """

        cursor.execute(query, )

        for row in cursor:
            result.append(Arco(idMapA[row["a1"]], idMapA[row["a2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

