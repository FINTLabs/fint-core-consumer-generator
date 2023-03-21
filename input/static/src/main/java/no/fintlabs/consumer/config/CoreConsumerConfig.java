package no.fintlabs.consumer.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

@Configuration
public class CoreConsumerConfig {

    @Qualifier("linkMapper")
    @Bean
    public Map<String, String> linkMapper() {
        return LinkMapper.linkMapper();
    }
}
