package com.socgame.campuswars_app.communication;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

public class HttpHeader {

    private HashMap<String, String> header;

    public HttpHeader(){
        header = new HashMap<String, String>();
        this.addUId();
    }

    public HashMap<String, String> getHeaders() {
        return header;
    }

    private void addUId(){
        //TODO add Uid, from Firebase
        header.put("UID", "42TODO13");
    }

    public void buildRoomFinderHeader(double latitude, double longitude){
        header.put("latitude", Double.toString(latitude));
        header.put("longitude", Double.toString(longitude));
    }

    public void buildPersonalLecturesHeader(JSONObject pLectures) throws JSONException {
        String lectures = "[";
        JSONArray arr = pLectures.getJSONObject("rowset").getJSONArray("row");

        for(int i = 0; i < arr.length(); i++){
            lectures += "\"" + arr.getJSONObject(i).get("stp_sp_titel") + ": " + arr.getJSONObject(i).get("semester_id") + "\",";
        }
        lectures += "]";
        header.put("Lectures", lectures);

        //Remove Log ?
        //Log.d("Test", header.toString());
    }

    public void buildGroupsHeader(){
        //TODO empty method stub
    }

    public void buildStartHeader(){
        //TODO empty method stub
    }

    public void buildQuestionHeader(){
        //TODO empty method stub
    }
}
