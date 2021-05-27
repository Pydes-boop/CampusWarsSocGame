package com.socgame.campuswars_app.communication;

import android.content.Context;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.net.MalformedURLException;
import java.net.URL;

public class HttpSingleton {
    //https://developer.android.com/training/volley/requestqueue
    private static HttpSingleton instance;
    private RequestQueue requestQueue;
    private static Context ctx;
    private static String url;

    private HttpSingleton(Context context) {
        ctx = context;
        requestQueue = getRequestQueue();
        url = "http://8.8.8.8:25565/";
    }

    public String getUrl(){
        return this.url;
    }

    /*
    public URL getUrl() throws MalformedURLException {
        return new URL(this.url);
    }*/

    public static synchronized HttpSingleton getInstance(Context context) {
        if (instance == null) {
            instance = new HttpSingleton(context);
        }
        return instance;
    }

    public RequestQueue getRequestQueue() {
        if (requestQueue == null) {
            // getApplicationContext() is key, it keeps you from leaking the
            // Activity or BroadcastReceiver if someone passes one in.
            requestQueue = Volley.newRequestQueue(ctx.getApplicationContext());
        }
        return requestQueue;
    }

    public <T> void addToRequestQueue(Request<T> req) {
        getRequestQueue().add(req);
    }

    public void getRequest(){
        Context context; //TODO add Context

        JsonArrayRequest jsonObjectRequest = new JsonArrayRequest
                (Request.Method.GET, this.url, null, new Response.Listener<JSONArray>() {

                    @Override
                    public void onResponse(JSONArray response) {
                        //TODO: On response
                        //textView.setText("Response: " + response.toString());
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO: Handle error

                    }
                });

        // Access the RequestQueue through your singleton class.
        // TODO: Add Context
        HttpSingleton.getInstance(null).addToRequestQueue(jsonObjectRequest);
    }

    public void postRequest(){
        //TODO: Post Request
    }



    //https://www.itsalif.info/content/android-volley-tutorial-http-get-post-put
    //https://stackoverflow.com/questions/33573803/how-to-send-a-post-request-using-volley-with-string-body

}
