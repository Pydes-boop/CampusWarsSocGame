package com.socgame.campuswars_app.communication;

import java.util.HashMap;

public class HttpHeader {

    private HashMap<String, String> header;

    public HttpHeader(){
        header = new HashMap<String, String>();
    }

    public HashMap<String, String> getHeaders() {
        return header;
    }

    public void addUId(){
        //TODO -> is this necessary? Should this be private?
    }

    public void buildRoomFinderHeader(double latitude, double longitude){
        header.put("latitude", Double.toString(latitude));
        header.put("longitude", Double.toString(longitude));
    }

    public void buildGroupsHeader(){
        //Use addUniqueID here?
    }

    public void buildStartHeader(){
        //TODO & discuss with backend
    }

    public void buildQuestionHeader(){
        //TODO & Discuss with backend
    }
}
