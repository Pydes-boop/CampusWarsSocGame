package com.socgame.campuswars_app.communication;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;

public class HttpReturn {

    private JSONArray arr;
    private RequestType type;

    private double latitude;
    private double longitude;

    public HttpReturn(RequestType type, JSONArray arr){
        this.type = type;
        this.arr = arr;
    }

    public void parseData() throws JSONException {
        //Does this make sense or do we have to solve this differently?
        switch(type){
            case ROOMDETECTION:
                break;
            case ROOMFINDER:
                break;
            case GROUPS:
                break;
            case QUESTION:
                break;
        }
    }

    private void parseRoomDetection(){
        for(int i = 0; i < this.arr.length(); i++){

        }
    }


    /*try {
        tet = test.parseData();
    } catch (JSONException e) {
        Log.d("JSON Error", e.toString());
    }
        for(int i = 0; i < tet.length(); i++){
        try {
            Log.d("JSON Test", tet.getJSONObject(i).toString());
            Log.d("JSON Test Location", tet.getJSONObject(i).get("location").toString());
        } catch (JSONException e) {
            Log.d("JSON Error", e.toString());
        }
    }*/
}
