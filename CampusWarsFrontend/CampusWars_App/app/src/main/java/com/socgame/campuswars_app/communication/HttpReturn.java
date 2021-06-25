package com.socgame.campuswars_app.communication;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;

public class HttpReturn {

    /**
     * currently unused, maybe will be used in the future again for easier/automatic processing of BackendCalls
     */

    private JSONArray arr;

    private double latitude;
    private double longitude;

    public HttpReturn(JSONArray arr){
        this.arr = arr;
    }

    public void parseData() throws JSONException {
        //Does this make sense or do we have to solve this differently?
        /*
        switch(type){
            case ROOMDETECTION:
                break;
            case QUESTION:
                break;
        }
        */
    }

    private void parseRoomDetection(){
        for(int i = 0; i < this.arr.length(); i++){

        }
    }
}
