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

public class Feiq {
    FeiqServer feiqServer;
    public Feiq() {
        feiqServer = new FeiqServer();
        feiqServer.setServerName("郭岩");
        feiqServer.setReceiveHandler(new LudaFeiQRobot(feiqServer));
        feiqServer.start();
    }

    public FeiqServer getFeiqServer() {
        return feiqServer;
    }
}
