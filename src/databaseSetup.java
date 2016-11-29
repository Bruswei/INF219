import java.sql.Statement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;

public class databaseSetup {
	
	private static Connection con;
	private static boolean hasData = false;
	
	public ResultSet displayMountains() throws SQLException, ClassNotFoundException
	{
		if (con == null)
			getConnection();
		
		Statement state = con.createStatement();
		ResultSet res = state.executeQuery("SELECT * FROM MOUNTAIN");
		
		return res;		
	}

	private void getConnection() throws ClassNotFoundException, SQLException {
		// TODO Auto-generated method stub
		
		Class.forName("org.sqlite.JDBC");
		con = DriverManager.getConnection("jdbc:sqlite:Mountains.db");
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
