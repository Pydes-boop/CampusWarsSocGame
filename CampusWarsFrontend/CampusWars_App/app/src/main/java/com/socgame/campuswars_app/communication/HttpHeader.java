package com.socgame.campuswars_app.communication;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.HashMap;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

public class HttpHeader {

    /**
     * This Class provides automatic processing/creation for HttpHeaders POST
     *
     * addUID, adds name and UID to every call for identification, gets added to probably all HttpPosts
     *
     * buildRoomFinderHeader, gives the Server our coordinates to get back if we are currently within a lecture hall
     *
     * buildPersonalLecturesHeader, creates a Header for sending our Backend all our Personal Lectures:
     * creates an Array filled with lectures uniquely identifiable by their Name + Semester
     * we sadly couldnt use the Tum Lecture Ids like "IN0011" because some lecturers dont provide them
     *
     * written by Daniel
     */

    private HashMap<String, String> header;
    private Context ctx;

    public HttpHeader(Context ctx){
        this.ctx = ctx;
        header = new HashMap<String, String>();
        this.addUId();
    }

    public HashMap<String, String> getHeaders() {
        return header;
    }

    //TODO FIX CALLS BECAUSE NO ONE EVER PROPERLY JUST GAVE ME AN EXAMPLE

    private void addUId(){
        SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
        String UID = settings.getString("UID", "empty");
        String name = settings.getString("name", "empty");
        String team = settings.getString("team", "no Team");
        header.put("uid", UID);
        header.put("name", name);
        header.put("team", team);
    }

    public void buildRoomFinderHeader(double latitude, double longitude){
        header.put("latitude", Double.toString(latitude));
        header.put("longitude", Double.toString(longitude));
    }

    public void buildPersonalLecturesHeader(JSONObject pLectures) throws JSONException {
        String lectures = "[";
        JSONArray arr = pLectures.getJSONObject("rowset").getJSONArray("row");

        lectures += "\"" + arr.getJSONObject(0).getString("stp_sp_titel").replace("\"", "").replace(":", "") + ": " + arr.getJSONObject(0).get("semester_id") + "\"";
        for(int i = 1; i < arr.length(); i++){
            lectures += ",\"" + arr.getJSONObject(i).getString("stp_sp_titel").replace("\"", "").replace(":", "") + ": " + arr.getJSONObject(i).get("semester_id") + "\"";
        }
        lectures += "]";
        header.put("lectures", lectures);
    }

    public void buildQuizHeader(double latitude, double longitude, String lid, String roomName){
        header.put("latitude", Double.toString(latitude));
        header.put("longitude", Double.toString(longitude));
        header.put("lid", lid);
        header.put("room", roomName);
    }
}
