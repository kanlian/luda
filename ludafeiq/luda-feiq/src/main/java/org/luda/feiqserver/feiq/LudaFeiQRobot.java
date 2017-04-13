package org.luda.feiqserver.feiq;
/*
 * Copyright 2017 Luda Team.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * Created by Him on 2017/4/13.
 */

import org.jplus.jfeiq.feiq.FeiqServer;
import org.jplus.jfeiq.feiq.IPMSGData;
import org.jplus.jfeiq.feiq.NetData;
import org.jplus.jfeiq.handler.SimpleReceiveHandler;

import java.util.regex.Pattern;

public class LudaFeiQRobot extends SimpleReceiveHandler {
    private final FeiqServer server;
    private static final String IP_REGEX = "((?:(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d)))\\.){3}(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d))))";
    private static final Pattern pattern = Pattern.compile(IP_REGEX);

    public LudaFeiQRobot(FeiqServer server) {
        super(server);
        this.server = server;
    }

    @Override
    public void dealWith(IPMSGData data) {
        super.dealWith(data);
        System.out.println("data = [" + data.toString() + "]");
        if (data.getCommandNo() == 288 || data.getCommandNo() == NetData.IPMSG_SENDMSG) {
            String msg = data.getAdditionalSection() + " -- FROM -- ";
            String ip = data.getIp();
            IPMSGData back = new IPMSGData(32, msg, ip);
            server.sendMsg(back);
        }
    }
}
